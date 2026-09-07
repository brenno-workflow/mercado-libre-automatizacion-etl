from .connection import get_connection

# Criar tabela
def create_tables():
    """
    Cria as tabelas necessárias para o ETL.
    """

    # TryCath
    try:

        # Conectar no banco
        __connection = get_connection()
        __cursor = __connection.cursor()

        __cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS etl_publications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                job_run DATETIME NOT NULL,
                product_id TEXT NOT NULL,
                product_name TEXT,
                item_id TEXT NOT NULL,
                seller_id INTEGER NOT NULL,
                price REAL,
                currency_id TEXT,
                currency_usd_rate REAL,
                price_usd REAL,
                condition TEXT,
                warranty TEXT,
                has_warranty BOOLEAN,
                listing_type_id TEXT,
                shipping_mode TEXT,
                shipping_logistic_type TEXT,
                shipping_free BOOLEAN,
                sold_quantity INTEGER
            )
            """
        )

        # Fechar
        __connection.commit()
        __connection.close()

    # Exception
    except Exception as e:
        print(f"Erro ao criar as tabelas no banco:\n{e}")
        return None