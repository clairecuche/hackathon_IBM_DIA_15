import os, requests

key = os.environ.get('IBM_API_KEY')
if not key:
    raise SystemExit('IBM_API_KEY not set')
r = requests.post('https://iam.cloud.ibm.com/identity/token', data={
    'apikey': key, 'grant_type': 'urn:ibm:params:oauth:grant-type:apikey'
})
print('status', r.status_code)
print(r.text)


import os
import requests
import json

# Récupère la clé depuis l'environnement (recommandé) ou remplace la valeur ci‑dessous pour test local
API_KEY = os.environ.get("IBM_API_KEY") or "<your api key>"

IAM_URL = "https://iam.cloud.ibm.com/identity/token"
DEPLOYMENT_URL = "https://eu-de.ml.cloud.ibm.com/ml/v4/deployments/2e248a30-ee3c-41eb-9025-7ec17fc4c731/predictions?version=2021-05-01"

# 1) Récupère le token IAM
try:
    token_resp = requests.post(
        IAM_URL,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={"apikey": API_KEY, "grant_type": "urn:ibm:params:oauth:grant-type:apikey"},
        timeout=10
    )
    print("IAM status:", token_resp.status_code)
    token_resp.raise_for_status()
    token = token_resp.json().get("access_token")
    if not token:
        print("Aucun access_token dans la réponse IAM:", token_resp.text)
        raise SystemExit(1)
except Exception as e:
    print("Erreur récupération token IAM:", e)
    raise

# 2) Construis le payload avec les colonnes nécessaires (une ligne d'exemple)
fields = [
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

# Exemple de valeurs correspondant à l'ordre ci‑dessous. Ajuste les valeurs réelles selon ton cas.
values = [
    [
        1,   # COLUMN1 (int example)
        0,   # prompt_speed_tps
        0,   # response_speed_tps
        0,   # load_duration
        0,   # total_inference_duration
        0,   # response_duration
        0,   # total_token_length
        0,   # response_token_length
        0,   # total_duration
        0,   # prompt_duration
        0,   # prompt_token_length
        0,   # model_name_encoded (int)
    ]
]

payload_scoring = {"input_data": [{"fields": fields, "values": values}]}

# 3) Appel du scoring
headers = {"Authorization": "Bearer " + token, "Content-Type": "application/json"}
try:
    r = requests.post(DEPLOYMENT_URL, json=payload_scoring, headers=headers, timeout=30)
    print("Scoring status:", r.status_code)
    try:
        print(json.dumps(r.json(), indent=2))
    except ValueError:
        print("Scoring non-JSON response:", r.text[:2000])
except requests.exceptions.RequestException as e:
    print("Erreur appel scoring :", type(e).__name__, e)
    print("Si l'URL commence par 'private.' elle peut ne pas être joignable depuis ta machine locale.")