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

Testing the IBM API and the backend
----------------------------------

This project calls an IBM Cloud Machine Learning deployment. If you think
the IBM call isn't working, follow these steps to verify connectivity and
credentials.

1) Make sure your API key is set in the environment on the machine running
   the server.

   - Bash (Linux / WSL / Git Bash):
     ```bash
     export IBM_API_KEY="<your-ibm-api-key>"
     ```
   - PowerShell (Windows):
     ```powershell
     $env:IBM_API_KEY = "<your-ibm-api-key>"
     ```

2) Verify IAM token retrieval (quick Python snippet).

   Save this as `backend/test_token.py` and run it with the same environment:

   ```python
   import os, requests

   key = os.environ.get('IBM_API_KEY')
   if not key:
       raise SystemExit('IBM_API_KEY not set')
   r = requests.post('https://iam.cloud.ibm.com/identity/token', data={
       'apikey': key, 'grant_type': 'urn:ibm:params:oauth:grant-type:apikey'
   })
   print('status', r.status_code)
   print(r.text)
   ```

   - Expected: 200 and a JSON containing `access_token`.
   - If you get 401/403/4xx, check that the API key is correct and not expired.

3) Confirm the deployment scoring endpoint is reachable from your machine.

   - The deployment URL is defined in `backend/ibm_client.py` as `DEPLOYMENT_URL`.
   - That URL may be a private endpoint (VPC). If it starts with `https://private...`
     it might only be reachable from inside the IBM Cloud or a configured network.
     In that case, your local machine will not be able to reach it; deploy
     the backend to an environment that can reach the endpoint or ask your
     cloud admin to allow access.

4) Try the scoring call directly (Python snippet). Replace `<your token>` with
   the access token retrieved in step 2 (or let the script fetch it).

   ```python
   import os, requests
   API_KEY = os.environ.get('IBM_API_KEY')
   token = requests.post('https://iam.cloud.ibm.com/identity/token', data={
       'apikey': API_KEY, 'grant_type': 'urn:ibm:params:oauth:grant-type:apikey'
   }).json()['access_token']

   headers = {'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json'}
   payload = {"input_data": [{"fields": ["prompt"], "values": [["Hello world"]]}]}
   url = 'REPLACE_WITH_DEPLOYMENT_URL_FROM_backend/ibm_client.py'
   r = requests.post(url, json=payload, headers=headers)
   print(r.status_code)
   try:
       print(r.json())
   except Exception:
       print(r.text)
   ```

   - Expected: a 200 with a JSON `predictions` array. If you get a 404/403 or
     a connection error, the deployment URL is not reachable from your host.

5) Test the local backend without calling IBM: provide metrics directly.

   If you want to test the backend routing and predictor without depending on
   IBM, POST metrics directly to `/predict` and include `total_inference_duration`.
   Example (curl):

   ```bash
   curl -X POST http://127.0.0.1:8000/predict \
     -H "Content-Type: application/json" \
     -d '{"prompt":"test","total_inference_duration":1.23,"prompt_token_length":10,"response_token_length":40,"model_name":"codellama:70b"}'
   ```

   The response should include a `consumption` object with `total_consumption` = 1.23.

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
