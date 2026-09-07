import os
from dotenv import load_dotenv
from .client import get_request

load_dotenv()

# Variaveis globais
ENDPOINT_CURRENCY = os.getenv("ML_CURRENCY")
ENDPOINT_SEARCH = os.getenv("ML_SEARCH")

# Buscar conversão de moeda
def extract_currency_conversion(url, from_currency, to_currency):
    """
    Busca a taxa de conversão entre duas moedas.
    """

    # TryCath
    try:

        __url = f"{url}/{ENDPOINT_CURRENCY}/{ENDPOINT_SEARCH}"
        __params = {"from": from_currency, "to": to_currency}
        __data = get_request(__url, params=__params)

        return __data

    # Exception
    except Exception as e:
        print(f"Erro ao buscar conversão de moeda: {e}")
        return None