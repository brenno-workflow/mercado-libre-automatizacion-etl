from .client import get_request

# Buscar detalhes do item
def extract_item_details(url, item_id):
    """
    Busca os detalhes de uma publicação no Mercado Livre.
    """

    # TryCath
    try:

        __url = f"{url}/items/{item_id}"
        __data = get_request(__url)

        return {
            "item_id": __data.get("id"),
            "seller_id": __data.get("seller_id"),
            "price": __data.get("price"),
            "currency_id": __data.get("currency_id"),
            "condition": __data.get("condition"),
            "sold_quantity": __data.get("sold_quantity"),
            "listing_type_id": __data.get("listing_type_id"),
            "shipping": __data.get("shipping"),
            "sale_terms": __data.get("sale_terms"),
        }

    # Exception
    except Exception as e:
        print(f"Erro ao buscar item {item_id}:\n{e}")
        return None