import requests
import json

URL = "https://localhost:8443/fs"  # our server only has POST /
REQ = {
    "op": "LIST",
    "path": "/"
}

resp = requests.post(
    URL,
    data=json.dumps(REQ),
    headers={"Content-Type": "application/json"},
    cert=("certs/nick.crt", "certs/nick.key"),  # client cert
    verify="certs/ca.crt"  # trust our CA
)

print(resp.status_code)
print(resp.text)