import os
from dotenv import load_dotenv
from .client import get_request

load_dotenv()

# Variaveis globais
ENDPOINT_PRODUCTS = os.getenv("ML_PRODUCTS")
ENDPOINT_SEARCH = os.getenv("ML_SEARCH")
ENDPOINT_ITEMS = os.getenv("ML_ITEMS")

# Buscar publicações
def extract_publications_active(url, query, site_id, limit, domain):
    """
    Busca anúncios no Mercado Livre Argentina.
    Considera somente produtos novos.
    """

    # TryCath
    try:

        # 1. Buscar produtos Samsung Galaxy
        __publications = []
        __url = f"{url}/{ENDPOINT_PRODUCTS}/{ENDPOINT_SEARCH}"
        __params = {
            "status": "active",
            "q": query,
            "site_id": site_id,
            "limit": limit,
            "offset": 0,
        }
        __data = get_request(__url, params=__params)
        __products = __data.get("results", [])
        print(f"Produtos encontrados: {len(__products)}")

        # 2. Buscar publicações de cada produto
        for __product in __products:

            # Verificar dominio
            if __product.get("domain_id") != domain:
                continue

            # Buscar ID do produto
            __product_id = __product["id"]
            __offset = 0
            while True:
                __url_items = (
                    f"{url}/{ENDPOINT_PRODUCTS}/"
                    f"{__product_id}/{ENDPOINT_ITEMS}"
                )
                __params_items = {"limit": limit, "offset": __offset}
                try: __data = get_request(__url_items, params=__params_items)
                except Exception as e: 
                    print(f"Erro ao buscar publicações do produto:\n{__product_id}: {e}")
                    break

                __items = __data.get("results", [])

                # Nenhum resultado = terminou a paginação
                if not __items:
                    break

                for __item in __items:

                    # Somente produtos novos
                    if __item.get("condition") != "new":
                        continue

                    __publications.append({
                        "product_id": __product_id,
                        "product_name": __product.get("name"),
                        "item_id": __item.get("item_id"),
                        "seller_id": __item.get("seller_id"),
                        "price": __item.get("price"),
                        "currency_id": __item.get("currency_id"),
                        "condition": __item.get("condition"),
                        "warranty": __item.get("warranty"),
                        "listing_type_id": __item.get("listing_type_id"),
                        "shipping": __item.get("shipping"),
                        "sale_terms": __item.get("sale_terms"),
                    })

                # Se menor que o limite = última página
                if len(__items) < int(limit):
                    break

                __offset += int(limit)

        return __publications

    # Exception
    except Exception as e:
        print(f"Erro ao buscar produtos:\n{e}")
        return None