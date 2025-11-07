"""Simple IBM ML client to call a deployment and extract metric fields.

This module expects the IBM API key to be provided via environment variable
`IBM_API_KEY`. It calls the IAM token endpoint, then the deployment scoring
endpoint (deployment URL is set below). It attempts to extract the following
metrics from the prediction response fields: 

prompt_speed_tps, response_speed_tps, load_duration, total_inference_duration,
response_duration, total_token_length, response_token_length, total_duration,
prompt_duration, prompt_token_length, model_name_encoded

If fields are not present in the model response, reasonable fallbacks are
applied (for token lengths we estimate from whitespace, others become None).

"""
from typing import Any, Dict, Optional, List
import os
import requests

# Replace with the deployment URL you provided
DEPLOYMENT_URL = (
    "https://eu-de.ml.cloud.ibm.com/ml/v4/deployments/2e248a30-ee3c-41eb-9025-7ec17fc4c731/predictions?version=2021-05-01"
)
IAM_TOKEN_URL = "https://iam.cloud.ibm.com/identity/token"

REQUIRED_METRICS = [
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


def get_token(api_key: str) -> str:
    """Retrieve IAM token from IBM Cloud using the API key."""
    data = {"apikey": api_key, "grant_type": "urn:ibm:params:oauth:grant-type:apikey"}
    resp = requests.post(IAM_TOKEN_URL, data=data, timeout=15)
    resp.raise_for_status()
    j = resp.json()
    return j["access_token"]


def score_prompt(
    prompt: Optional[str] = None,
    api_key: Optional[str] = None,
    fields: Optional[List[str]] = None,
    values: Optional[List[List[Any]]] = None,
) -> Dict[str, Any]:
    """Send data to the deployment and return the raw JSON response.

    You can either provide `prompt` (the helper will send a single-field
    payload with field name "prompt") or provide `fields` and `values`
    explicitly to match the deployment's expected input schema.
    """
    if api_key is None:
        api_key = os.environ.get("IBM_API_KEY")
    if not api_key:
        raise RuntimeError("IBM_API_KEY environment variable must be set")

    token = get_token(api_key)
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    # Build payload: prefer explicit fields/values if provided
    if fields is not None and values is not None:
        payload_scoring = {"input_data": [{"fields": fields, "values": values}]}
    else:
        # fallback to a single 'prompt' field
        payload_scoring = {"input_data": [{"fields": ["prompt"], "values": [[prompt]]}]}

    resp = requests.post(DEPLOYMENT_URL, json=payload_scoring, headers=headers, timeout=30)
    # don't raise here - caller may want to inspect response content
    try:
        return resp.json()
    except ValueError:
        # non-json body
        return {"raw_text": resp.text, "status_code": resp.status_code}


def extract_metrics(prediction_response: Dict[str, Any], prompt: Optional[str] = None) -> Dict[str, Optional[Any]]:
    """Extract required metrics from the IBM predictions response.

    The IBM WML prediction response often looks like:
    {"predictions": [{"fields": [...], "values": [[...]]}]}

    We'll map field names to their values and then pick out the required metrics.
    If a metric is missing, we provide a fallback or None.
    """
    out: Dict[str, Optional[Any]] = {k: None for k in REQUIRED_METRICS}

    preds = prediction_response.get("predictions")
    if not preds or not isinstance(preds, list):
        # nothing to extract
        # try looking for a top-level mapping of metrics
        for k in REQUIRED_METRICS:
            if k in prediction_response:
                out[k] = prediction_response[k]
        # add approximate token length if prompt provided
        if prompt and out.get("prompt_token_length") is None:
            out["prompt_token_length"] = _estimate_tokens(prompt)
        return out

    first = preds[0]
    fields = first.get("fields") or []
    values = None
    vals = first.get("values")
    if vals and isinstance(vals, list) and len(vals) > 0:
        values = vals[0]

    mapping: Dict[str, Any] = {}
    if fields and values:
        for name, val in zip(fields, values):
            mapping[name] = val

    # copy known metrics from mapping
    for k in REQUIRED_METRICS:
        if k in mapping:
            out[k] = mapping[k]

    # fallback for prompt token length
    if out.get("prompt_token_length") is None and prompt:
        out["prompt_token_length"] = _estimate_tokens(prompt)

    return out


def _estimate_tokens(text: str) -> int:
    """Very small approximation for token count: whitespace split.

    This is NOT an exact tokenization for any specific LLM tokenizer, but is
    a fast fallback when the model did not return token counts.
    """
    if not text:
        return 0
    return len(text.split())


if __name__ == "__main__":
    # quick manual test
    import json
    s = score_prompt("Hello world")
    print(json.dumps(s, indent=2))
