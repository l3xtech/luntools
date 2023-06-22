import requests
from msal import ConfidentialClientApplication

def acessar_api_defender(tenant_id, client_id, client_secret, endpoint):
    authority = f"https://login.microsoftonline.com/{tenant_id}"

    app = ConfidentialClientApplication(
        client_id,
        authority=authority,
        client_credential=client_secret,
    )

    result = None
    result = app.acquire_token_silent(["https://api.securitycenter.windows.com/.default"], account=None)

    if not result:
        print("Fazendo solicitação para obter token...")
        result = app.acquire_token_for_client(scopes=["https://api.securitycenter.windows.com/.default"])

    if "access_token" in result:
        headers = {
            'Authorization': 'Bearer ' + result['access_token'],
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

        response = requests.get(endpoint, headers=headers)

        if response.status_code == 200:
            print(response.json())
        else:
            print(f"Erro na solicitação: {response.status_code}")
    else:
        print(f"Erro na autenticação: {result.get('error')}, {result.get('error_description')}")

# Substitua os valores pelas suas chaves
tenant_id = "your_tenant_id"
client_id = "your_client_id"
client_secret = "your_client_secret"
endpoint = "your_endpoint"

acessar_api_defender(tenant_id, client_id, client_secret, endpoint)
