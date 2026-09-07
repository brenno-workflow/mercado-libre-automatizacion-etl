import pandas as pd

# Tabular
def transform_to_dataframe(publications, currency_rate=None):
    """
    Transforma as publicações extraídas em uma estrutura tabular (dataframe).
    """

    # Trycath
    try:

        # Buscar informações
        __data = []
        for __publication in publications:

            # Buscar infos
            __shipping = __publication.get("shipping") or {}
            __warranty = __publication.get("warranty") or ""
            __has_warranty = __warranty.lower() != "sin garantía"
            __price_usd = __publication.get("price") * currency_rate if __publication.get("price") is not None and currency_rate is not None else None

            # Adicionar a lista
            __data.append({
                "product_id": __publication.get("product_id"),
                "product_name": __publication.get("product_name"),
                "item_id": __publication.get("item_id"),
                "seller_id": __publication.get("seller_id"),
                "price": __publication.get("price"),
                "currency_id": __publication.get("currency_id"),
                "condition": __publication.get("condition"),
                "warranty": __publication.get("warranty"),
                "has_warranty": __has_warranty,
                "listing_type_id": __publication.get("listing_type_id"),
                "shipping_mode": __shipping.get("mode"),
                "shipping_logistic_type": __shipping.get("logistic_type"),
                "shipping_free": __shipping.get("free_shipping"),
                "currency_usd_rate": currency_rate,
                "price_usd": __price_usd,
                "sold_quantity": __publication.get("sold_quantity"),
            })

        # Criar dataframe
        __df = pd.DataFrame(__data)
        return __df

    # Exception
    except Exception as e:
        print(f"Erro ao tarnsformar os dados:\n{e}")
        return None