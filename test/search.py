import os
import requests
from dotenv import load_dotenv

load_dotenv()

# Vaariaveis globais
TOKEN = os.getenv("ML_ACCESS_TOKEN")
ML_PAGE_SIZE = os.getenv("ML_PAGE_SIZE")
ML_MAX_RECORDS = os.getenv("ML_MAX_RECORDS")

# Buscar items
def search_items(url, query):
    """
    Busca anúncios no Mercado Livre Argentina.
    """

    # TryCath
    try:

        # URL
        __url = url + "/search"

        # Headers
        __headers = {"Authorization": f"Bearer {TOKEN}"}

        # Params
        __params = {"q": query, "limit": 50, "offset": 0}
        #__params = {"sellerid": 1156343076}

        # Requisição
        __response = requests.get(__url, headers=__headers, params=__params)
        __response.raise_for_status()
        __response = __response.json()
        print(__response)

        # Return
        return __response

    # Exception
    except Exception as e:
        print(f"Erro ao buscar produtos:\n{e}")
        return None