from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional, List
import os
import traceback

from . import ibm_client
from . import energy
from . import predictor

# Map human-friendly model names to integer codes used by your model
MODEL_NAME_MAP = {
    "codellama": 0,
    "codellama:70b": 1,
    "codellama:7b": 2,
    "gemma:2b": 3,
    "gemma:7b": 4,
    "llama3": 5,
    "llama3:70b": 6,
}

# Fixed input_fields order expected by the deployment (must be sent in this
# exact order). We always format the scoring payload using this order so the
# server will behave like the working `tests/test_token.py` script.
FIXED_INPUT_FIELDS = [
    "COLUMN1",
    "prompt_speed_tps",
    "response_speed_tps",
    "load_duration",
    "total_inference_duration",
    "response_duration",
    "total_token_length",
    "response_token_length",
    "total_duration",
    "prompt_duration",
    "prompt_token_length",
    "model_name_encoded",
]

app = FastAPI(title="LLM Consumption Predictor")


class PredictRequest(BaseModel):
    
    prompt: Optional[str] = None

    
    prompt_speed_tps: Optional[float] = None
    response_speed_tps: Optional[float] = None
    load_duration: Optional[float] = None
    total_inference_duration: Optional[float] = None
    response_duration: Optional[float] = None
    total_token_length: Optional[int] = None
    response_token_length: Optional[int] = None
    total_duration: Optional[float] = None
    prompt_duration: Optional[float] = None
    prompt_token_length: Optional[int] = None
   
    model_name_encoded: Optional[str] = None
    model_name: Optional[str] = None

    country: Optional[str] = None


class PredictResponse(BaseModel):
    raw_response: Optional[Dict[str, Any]] = None

@app.get("/")
def root():
    """Simple root to make visiting / in a browser useful instead of 404."""
    return {
        "message": "LLM Consumption Predictor",
        "endpoints": {
            "predict": {
                "method": "POST",
                "path": "/predict",
                "description": "Send JSON {\"prompt\":..., \"energy_mix\": {...}}",
            },
            "docs": {"path": "/docs", "description": "Interactive OpenAPI docs"},
        },
    }


@app.get("/favicon.ico")
def favicon():
    # return no content to avoid 404 in browser logs
    from fastapi.responses import Response

    return Response(status_code=204)


@app.post("/predict", response_model=PredictResponse)
def predict(req: PredictRequest):
    # ensure API key available
    # If the client provided metric fields directly, use them and skip the
    # IBM call. Otherwise, if a prompt is present, call the IBM deployment to
    # obtain metrics. If neither metrics nor prompt are provided, return an
    # error.

    raw = None

    def build_ordered_values():
        # If client provided raw input_values, try to reorder them to the
        # FIXED_INPUT_FIELDS order.
        if getattr(req, "input_values", None):
            provided_fields = getattr(req, "input_fields", None) or []
            # take only the first row if multiple provided, and map by index
            provided_row = req.input_values[0] if req.input_values else []
            # Build a row following FIXED_INPUT_FIELDS by matching indexes
            ordered_row = []
            for f in FIXED_INPUT_FIELDS:
                if f in provided_fields:
                    idx = provided_fields.index(f)
                    # safe-get value from provided_row
                    try:
                        ordered_row.append(provided_row[idx])
                    except Exception:
                        ordered_row.append(0)
                else:
                    # field not present in provided_fields -> fill from
                    # explicit metric attributes or sensible defaults
                    if f == "COLUMN1":
                        ordered_row.append(1)
                    elif f == "model_name_encoded":
                        # prefer explicit numeric encoded value, else map name
                        if getattr(req, "model_name_encoded", None) is not None:
                            ordered_row.append(req.model_name_encoded)
                        elif getattr(req, "model_name", None):
                            code = MODEL_NAME_MAP.get(req.model_name.strip().lower())
                            ordered_row.append(code if code is not None else 0)
                        else:
                            ordered_row.append(0)
                    else:
                        val = getattr(req, f, None)
                        ordered_row.append(val if val is not None else 0)
            return [ordered_row]

        # No input_values provided: build from individual metric fields
        row = []
        for f in FIXED_INPUT_FIELDS:
            if f == "COLUMN1":
                row.append(1)
                continue
            if f == "model_name_encoded":
                if getattr(req, "model_name_encoded", None) is not None:
                    row.append(req.model_name_encoded)
                elif getattr(req, "model_name", None):
                    code = MODEL_NAME_MAP.get(req.model_name.strip().lower())
                    row.append(code if code is not None else 0)
                else:
                    row.append(0)
                continue
            # other numeric metric fields
            row.append(getattr(req, f, 0) or 0)

        return [row]

    # Always call IBM with the fixed fields/ordered values
    api_key = os.environ.get("IBM_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="IBM_API_KEY not set in environment")
    try:
        values = build_ordered_values()
        raw = ibm_client.score_prompt(
            prompt=None,
            api_key=api_key,
            fields=FIXED_INPUT_FIELDS,
            values=values,
        )
    except Exception as e:
        tb = traceback.format_exc()
        raise HTTPException(status_code=502, detail=f"Error calling IBM ML: {e}\n{tb}")

    metrics = ibm_client.extract_metrics(raw, prompt=req.prompt)
    # If the request included a human-readable model_name or an explicit
    # model_name_encoded prefer those values to override the scored output.
    if req.model_name:
        code = MODEL_NAME_MAP.get(req.model_name.strip().lower())
        if code is not None:
            metrics["model_name_encoded"] = code
    if getattr(req, "model_name_encoded", None) is not None:
        metrics["model_name_encoded"] = getattr(req, "model_name_encoded")

    # Determine energy mix: prefer explicit energy_mix from client, else
    # compute from provided country, else None
    computed_mix = None
    computed_mix = energy.get_energy_mix_for_country(req.country)

    resp = {
        "raw_response": raw,
    }

    # extract total consumption reported by the model (seconds) and attach
    try:
        consumption = predictor.extract_total_consumption(metrics, raw_response=raw)
        resp["consumption"] = consumption
    except Exception:
        resp["consumption"] = {"total_consumption": None, "units": "seconds", "source_field": None}

    return resp


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.app:app", host="0.0.0.0", port=8000, reload=True)
