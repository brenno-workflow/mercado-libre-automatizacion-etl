from .connection import get_connection

# Carregar dados no banco
def load_publications(dataframe):
    """
    Insere as publicações no banco SQLite.
    """

    # TryCath
    try:

        __connection = get_connection()
        __dataframe = dataframe.copy()

        __dataframe.to_sql(
            "etl_publications",
            __connection,
            if_exists="append",
            index=False
        )

        __connection.close()

    # Exception
    except Exception as e:
        print(f"Erro ao inserir os dados no banco:\n{e}")
        return None