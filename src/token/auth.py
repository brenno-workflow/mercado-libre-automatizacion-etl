import os
import requests
from dotenv import load_dotenv, set_key

load_dotenv()

# Variaveis globais
#ML_URL = os.getenv("ML_URL_API") + os.getenv("ML_AUTH")
ENDPOINT_AUTHS = os.getenv("ML_AUTH")
ML_APP_ID = os.getenv("ML_APP_ID")
ML_CLIENT_SECRET = os.getenv("ML_CLIENT_SECRET")
ML_REFRESH_TOKEN = os.getenv("ML_REFRESH_TOKEN")

# Atualizar token
def refresh_access_token(url):
    """
    Atualiza o token para consulta da API
    """

    # TryCath
    try:

        # URL
        __url = f"{url}/{ENDPOINT_AUTHS}"

        # Header
        __headers = {
            'accept': 'application/json',
            'content-type': 'application/x-www-form-urlencoded'
        }

        # Payload
        __payload = {
            "grant_type": "refresh_token",
            "client_id": ML_APP_ID,
            "client_secret": ML_CLIENT_SECRET,
            "refresh_token": ML_REFRESH_TOKEN,
        }

        # Requisição
        __response = requests.post(__url, headers=__headers , data=__payload)
        __response.raise_for_status()
        __response = __response.json()

        # Atualizar .env
        set_key(".env", "ML_ACCESS_TOKEN", __response["access_token"])
        set_key(".env", "ML_REFRESH_TOKEN", __response["refresh_token"])

        # Return
        return __response
    
    # Exception
    except Exception as e:
        print(f"Erro ao atualizar o token:\n{e}")
        return None

#refresh_access_token()