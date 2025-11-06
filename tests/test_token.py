import os, requests

key = os.environ.get('IBM_API_KEY')
if not key:
    raise SystemExit('IBM_API_KEY not set')
r = requests.post('https://iam.cloud.ibm.com/identity/token', data={
    'apikey': key, 'grant_type': 'urn:ibm:params:oauth:grant-type:apikey'
})
print('status', r.status_code)
print(r.text)