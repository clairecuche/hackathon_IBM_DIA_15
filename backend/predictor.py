"""Predictor utilities: estimate energy consumption and CO2e and track predictions.

This is a pragmatic estimator that uses available metrics (durations, token
counts, speeds) and falls back to model-based throughput and power assumptions
when metrics are missing. All numeric values are estimates and must be tuned
with real profiling data for production use.
"""
from typing import Dict, Any, Optional
import time
import csv
import os
import json

# rough average power draw (Watts) per model code. These are conservative
# placeholders and should be replaced with measured values for accuracy.
MODEL_POWER_WATTS = {
    0: 50,   # codellama (small)
    1: 300,  # codellama:70b
    2: 150,  # codellama:7b
    3: 120,  # gemma:2b
    4: 200,  # gemma:7b
    5: 350,  # llama3
    6: 700,  # llama3:70b
}

# default throughput (tokens per second) per model code when no speed metrics
# are provided. These are coarse estimates.
MODEL_TOKENS_PER_SEC = {
    0: 200,  # codellama
    1: 50,   # codellama:70b
    2: 120,  # codellama:7b
    3: 180,  # gemma:2b
    4: 100,  # gemma:7b
    5: 40,   # llama3 (large)
    6: 15,   # llama3:70b (very large)
}

# emission factors (kgCO2e per kWh) by energy source (literature approximations)
EMISSION_FACTORS = {
    "coal": 0.820,
    "gas": 0.490,
    "nuclear": 0.012,
    "renewables": 0.050,
    "solar": 0.05,
    "wind": 0.05,
    "grid": 0.5,
}

LOG_DIR = os.path.join(os.path.dirname(__file__), "logs")
LOG_FILE = os.path.join(LOG_DIR, "predictions.csv")


def _ensure_log():
    os.makedirs(LOG_DIR, exist_ok=True)
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                "ts",
                "model_name",
                "model_code",
                "prompt_tokens",
                "response_tokens",
                "total_tokens",
                "duration_s",
                "energy_kwh",
                "energy_joules",
                "co2_kg",
                "country",
                "energy_mix",
                "raw_metrics",
            ])


def _compute_grid_emission_factor(energy_mix: Optional[Dict[str, float]]) -> float:
    if not energy_mix:
        return EMISSION_FACTORS["grid"]
    total = 0.0
    for src, share in energy_mix.items():
        ef = EMISSION_FACTORS.get(src.lower(), EMISSION_FACTORS.get("grid", 0.5))
        total += ef * float(share)
    return total


def extract_total_consumption(metrics: Dict[str, Any], raw_response: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Extract the model-reported total consumption (duration) from metrics or raw response.

    Priority of fields to use (first found):
      - total_inference_duration
      - total_duration
      - total_time
      - response_duration
      - sum of prompt_duration + response_duration

    Returns a dict with keys:
      - total_consumption (float, seconds) or None
      - units: 'seconds'
      - source_field: which field was used
    """
    # look directly in metrics first
    candidates = ["total_inference_duration", "total_duration", "total_time", "response_duration"]
    for f in candidates:
        v = metrics.get(f)
        if v is not None:
            try:
                return {"total_consumption": float(v), "units": "seconds", "source_field": f}
            except Exception:
                pass

    # if not in metrics, try raw_response structure (IBM style)
    if raw_response and isinstance(raw_response, dict):
        # try top-level keys
        for f in candidates:
            v = raw_response.get(f)
            if v is not None:
                try:
                    return {"total_consumption": float(v), "units": "seconds", "source_field": f}
                except Exception:
                    pass

        # fall back to checking predictions -> fields/values mapping
        preds = raw_response.get("predictions")
        if preds and isinstance(preds, list) and len(preds) > 0:
            first = preds[0]
            fields = first.get("fields") or []
            vals = None
            if first.get("values") and len(first.get("values")) > 0:
                vals = first.get("values")[0]
            if fields and vals:
                mapping = {name: val for name, val in zip(fields, vals)}
                for f in candidates:
                    if f in mapping:
                        try:
                            return {"total_consumption": float(mapping[f]), "units": "seconds", "source_field": f}
                        except Exception:
                            pass

    # as a last resort, try summing prompt_duration + response_duration
    pd = metrics.get("prompt_duration")
    rd = metrics.get("response_duration")
    try:
        if pd is not None and rd is not None:
            return {"total_consumption": float(pd) + float(rd), "units": "seconds", "source_field": "prompt_duration+response_duration"}
    except Exception:
        pass

    # nothing found
    return {"total_consumption": None, "units": "seconds", "source_field": None}
