# Backend: IBM ML consumption predictor

This small backend exposes a POST /predict endpoint that:

- sends the provided `prompt` to an IBM Cloud Machine Learning deployment
- extracts LLM consumption metrics from the deployment prediction response
- returns those metrics together with the user-provided `energy_mix`

Requirements
- Python 3.10+
- Set environment variable `IBM_API_KEY` to your IBM Cloud API key.

Install

```bash
python -m venv .venv
source .venv/bin/activate    # on Windows use: .venv\Scripts\activate
pip install -r backend/requirements.txt
```

Run

```bash
export IBM_API_KEY="IAM"   # PowerShell: $env:IBM_API_KEY = "<your key>"
uvicorn backend.app:app --host 0.0.0.0 --port 8000 --reload
```


Troubleshooting tips
- If token retrieval fails: re-create the API key in IBM Cloud and ensure it
  has the ML service access permissions.
- If scoring call returns 401: the token is invalid/expired — re-run the token
  request and use the returned token.
- If scoring call returns 404 or connection refused: the deployment URL is
  unreachable (often because it's a private URL). Confirm whether the URL
  is public or requires a VPN / IBM Cloud network.
- Check the server logs where you run `uvicorn` for stack traces and raw
  `response_scoring.text` prints from `backend/ibm_client.py`.

Where to look for diagnostics
- Backend logs: the terminal running `uvicorn` will show HTTP errors and
  stack traces.
- Prediction tracking: `backend/logs/predictions.csv` (when running predictor
  logging) will contain rows of observed predictions.


Notes
- The `ibm_client` module attempts to map prediction `fields` -> `values` and
  extract the requested metric names. If the deployment does not return those
  fields, some metrics will be `null` and token counts fall back to a simple
  whitespace-based estimate.
