import os
import requests
from dotenv import load_dotenv

from src.token.auth import refresh_access_token
from src.api.search import search_items
from src.api.products import extract_publications_active
from src.database.transform import transform_to_dataframe

load_dotenv()

# Variaveis globais
ML_URL = os.getenv("ML_URL", "https://api.mercadolibre.com")
ML_SITE_ID = os.getenv("ML_SITE_ID")
ML_SEARCH_QUERY = os.getenv("ML_SEARCH_QUERY")
ML_SEARCH_DOMAIN = os.getenv("ML_SEARCH_DOMAIN")
ML_SEARCH_PAGE_SIZE = os.getenv("ML_SEARCH_PAGE_SIZE")

# Gerar base
def main():
    
    # Atualizar token
    refresh_access_token(url=ML_URL)

    # Buscar item
    __search_data = extract_publications_active(url=ML_URL, query=ML_SEARCH_QUERY, site_id=ML_SITE_ID, limit=ML_SEARCH_PAGE_SIZE, domain=ML_SEARCH_DOMAIN)
    print(f"Publicações extraídas: {len(__search_data)}")

    # Trnsformar
    __df = transform_to_dataframe(__search_data)
    print(__df)

    for publication in __search_data:
        print(
            f"Produto: {publication['product_name']}\n"
            f"Item: {publication['item_id']}\n"
            f"Seller: {publication['seller_id']}\n"
            f"Preço: {publication['price']} {publication['currency_id']}\n"
            f"Garantia: {publication['warranty']}\n"
            f"Frete: {publication['shipping']['logistic_type']}\n"
            f"Frete grátis: {publication['shipping']['free_shipping']}\n"
            f"{'-' * 60}"
        )

if __name__ == "__main__":
    main()