import requests
import json
from datetime import date
from azure.identity import ClientSecretCredential

# Configure suas credenciais do Azure AD
tenant_id = 'YOUR_TENANT_ID'
client_id = 'YOUR_CLIENT_ID'
client_secret = 'YOUR_CLIENT_SECRET'

# Crie uma instância do ClientSecretCredential
credential = ClientSecretCredential(tenant_id, client_id, client_secret)

# Obtenha um token de acesso
token = credential.get_token('https://api.security.microsoft.com/.default')

# Crie o cabeçalho para a solicitação
headers = {
    'Authorization': 'Bearer ' + token.token,
    'Accept': 'application/json',
}

# Define a URL base da API do Microsoft 365 Defender
base_url = 'https://api.security.microsoft.com'

# Faça a solicitação para a API
response = requests.get(base_url + '/api/alerts', headers=headers)

# Verifique se a solicitação foi bem-sucedida
if response.status_code == 200:
    data = response.json()

    # Define o nome do arquivo com a data de hoje
    filename = f'defender_{date.today().isoformat()}.json'

    # Salva os dados em um arquivo JSON
    with open(filename, 'w') as f:
        json.dump(data, f)

else:
    print(f'Error: {response.status_code}')

