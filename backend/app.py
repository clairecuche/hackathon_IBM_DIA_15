"""FastAPI app exposing /predict that uses the IBM deployment to score prompts
and returns the requested LLM consumption metrics together with the user
provided energy mix.

Usage:
  export IBM_API_KEY="<your api key>"
  uvicorn backend.app:app --reload --port 8000

POST /predict
  body: {"prompt": "...", "energy_mix": {"solar": 0.5, "wind": 0.3, "grid": 0.2}}
  returns: {"metrics": {...}, "energy_mix": {...}, "raw_response": {...}}

"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional
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

app = FastAPI(title="LLM Consumption Predictor")


class PredictRequest(BaseModel):
    # Optional prompt text. If provided and no metric fields are supplied the
    # server will call the IBM deployment to obtain metrics. If metrics are
    # supplied directly (see fields below) the server will use those values
    # instead and skip the IBM call.
    prompt: Optional[str] = None

    # Metric fields (all optional) — client may supply these directly.
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
    # allow client to provide a model name which will be mapped to an integer
    # code using MODEL_NAME_MAP. If the client supplies model_name_encoded
    # directly it will be used as-is.
    model_name_encoded: Optional[str] = None
    model_name: Optional[str] = None

    # the client can either provide an explicit energy_mix, or provide a
    # `country` and we'll compute a representative energy mix server-side.
    country: Optional[str] = None


class PredictResponse(BaseModel):
    metrics: Dict[str, Optional[Any]]
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

    # Build metrics from request fields if any metric is present
    metric_fields = [
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

    provided_any_metric = any(getattr(req, f) is not None for f in metric_fields)

    raw = None
    metrics: Dict[str, Optional[Any]] = {k: None for k in metric_fields}

    if provided_any_metric:
        for f in metric_fields:
            metrics[f] = getattr(req, f)
        # if client provided a human-friendly model_name, map it to an int
        if req.model_name:
            code = MODEL_NAME_MAP.get(req.model_name.strip().lower())
            # only set when mapping exists
            if code is not None:
                metrics["model_name_encoded"] = code
        # if client provided model_name_encoded explicitly, prefer that
        if getattr(req, "model_name_encoded", None) is not None:
            metrics["model_name_encoded"] = getattr(req, "model_name_encoded")
    else:
        # need prompt to call IBM
        if not req.prompt:
            raise HTTPException(status_code=400, detail="Either supply metric fields or a prompt to score")

        api_key = os.environ.get("IBM_API_KEY")
        if not api_key:
            raise HTTPException(status_code=500, detail="IBM_API_KEY not set in environment")

        try:
            raw = ibm_client.score_prompt(req.prompt, api_key=api_key)
        except Exception as e:
            tb = traceback.format_exc()
            raise HTTPException(status_code=502, detail=f"Error calling IBM ML: {e}\n{tb}")

        metrics = ibm_client.extract_metrics(raw, prompt=req.prompt)
        # if the client supplied a human model_name along with the prompt
        # use it to override model_name_encoded if mapping exists
        if req.model_name:
            code = MODEL_NAME_MAP.get(req.model_name.strip().lower())
            if code is not None:
                metrics["model_name_encoded"] = code

    # Determine energy mix: prefer explicit energy_mix from client, else
    # compute from provided country, else None
    computed_mix = None
    computed_mix = energy.get_energy_mix_for_country(req.country)

    resp = {
        "metrics": metrics,
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
