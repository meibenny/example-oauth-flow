import json
import requests
import sys
import time
import uuid

REALM = "master"
BASE_URL = "http://localhost:8080"
CREATE_CLIENT_URL = f"{BASE_URL}/admin/realms/{REALM}/clients"
OPENTOKEN_URL = f"{BASE_URL}/realms/{REALM}/protocol/openid-connect/token"
HEALTHCHECK_ENDPOINT = f"{BASE_URL}/health/ready"
client_id = uuid.uuid4()


keycloak_starting = True
start_time = time.time()
while(keycloak_starting):
    try:
        resp = requests.get(HEALTHCHECK_ENDPOINT, timeout=5)
        resp.raise_for_status
        keycloak_starting = False
    except:
        print("keycloak not ready yet")
        time_now = time.time()
        elapsed = time_now - start_time
        if (elapsed > 120):
            sys.exit("keycloak unhealthy")
        time.sleep(2)

# get access token so we can interact with the API
request_body = {
    "client_id": "admin-cli",
    "username": "admin",
    "password": "admin",
    "grant_type": "password"
}

resp = requests.post(OPENTOKEN_URL, data=request_body)
access_token = resp.json().get("access_token")
print(f"retrieved access token")

# create our client
redirectUris = ["http://localhost:8000/authorize"]
headers = {
    "Authorization": f"bearer {access_token}"
}
client_representation = {
    "id": str(client_id),
    "clientId": str(client_id),
    "name": str(client_id),
    "standardFlowEnabled": True,
    "publicClient": False,
    "redirectUris": redirectUris,
}

resp = requests.post(CREATE_CLIENT_URL, headers=headers, json=client_representation)
print(f"created client {client_id}")

# get the client secret
URL = CREATE_CLIENT_URL + f"/{str(client_id)}"
resp = requests.get(URL, headers=headers)
client_secret = resp.json().get("secret")
print("retrieved client secret")

results = {
    "web": {
        "client_id": str(client_id),
        "client_secret": client_secret,
        "auth_uri": "http://localhost:8080/authorize",
        "userinfo_url": "http://localhost:8080/realms/master/protocol/openid-connect/userinfo",
        "issuer": "http://localhost:8080/realms/master",
        "redirect_uris": redirectUris
    }
}
with open("client_secrets.json", "w") as f:
    f.write(json.dumps(results, indent=4))
print(results)