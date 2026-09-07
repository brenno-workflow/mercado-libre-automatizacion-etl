import os
from dotenv import load_dotenv
from datetime import datetime

from src.token.auth import refresh_access_token
from src.api.products import extract_publications_active
from src.api.items import extract_item_details
from src.api.currencies import extract_currency_conversion
from src.database.models import create_tables
from src.database.transform import transform_to_dataframe
from src.database.load import load_publications

load_dotenv()

# Variaveis globais
ML_URL = os.getenv("ML_URL", "https://api.mercadolibre.com")
ML_SITE_ID = os.getenv("ML_SITE_ID")
ML_SEARCH_QUERY = os.getenv("ML_SEARCH_QUERY")
ML_SEARCH_DOMAIN = os.getenv("ML_SEARCH_DOMAIN")
ML_SEARCH_PAGE_SIZE = os.getenv("ML_SEARCH_PAGE_SIZE")

# Gerar base
def main():

    # TryCath
    try:

        # Identificador da execução do ETL
        __job_run = datetime.now()

        # Criar estrutura do banco
        create_tables()
        
        # Atualizar token
        refresh_access_token(url=ML_URL)
        
        # Buscar item
        __search_data = extract_publications_active(url=ML_URL, query=ML_SEARCH_QUERY, site_id=ML_SITE_ID, limit=ML_SEARCH_PAGE_SIZE, domain=ML_SEARCH_DOMAIN)
        print(f"Publicações extraídas: {len(__search_data)}")

        # Enriquecer dados dos itens
        for __publication in __search_data:
            __item_id = __publication.get("item_id")

            # Verificar se existe
            if not __item_id:
                continue

            # Buscar detalhes
            __item_data = extract_item_details(url=ML_URL, item_id=__item_id)
            if __item_data:
                __publication.update(__item_data)

        # Buscar valor USD
        __conversion = extract_currency_conversion(url=ML_URL, from_currency="ARS", to_currency="USD")
        __currency_rate = None
        if __conversion:
            __currency_rate = __conversion.get("rate")

        # Trnsformar
        __df = transform_to_dataframe(__search_data, __currency_rate)

        # Adicionar identificador da execução
        __df["job_run"] = __job_run

        # Carregar dados no banco
        load_publications(__df)

        print("Dados carregados no banco com sucesso.")

    # Exception
    except Exception as e:
        print(f"Erro ao rodar a automação:\n{e}")
        return None

def main2():
    __conversion = extract_currency_conversion(
        url=ML_URL,
        from_currency="ARS",
        to_currency="USD"
    )

    print("\nConversão ARS -> USD:")
    print(__conversion)

main()