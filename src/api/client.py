import os
import requests

# Headers
def get_headers():
    """
    Retorna os headers utilizando o token de acesso atual.
    """
    token = os.getenv("ML_ACCESS_TOKEN")

    return {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0",
    }

# GET
def get_request(url, params=None):
    """
    Realiza uma requisição GET para a API do Mercado Livre.
    """

    response = requests.get(
        url,
        headers=get_headers(),
        params=params,
        timeout=15,
    )

    response.raise_for_status()

    return response.json()