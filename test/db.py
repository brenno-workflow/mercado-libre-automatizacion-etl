#from .connection import get_connection
import sqlite3

# Exibir banco salvo
def check_database():
    """
    Exibe informações básicas do banco.
    """

    #__connection = get_connection()
    __connection = sqlite3.connect('mercado_livre.db')
    __cursor = __connection.cursor()

    # Vendedores com múltiplas publicações
    __cursor.execute("""
        SELECT
    shipping_mode,
    shipping_logistic_type,
    shipping_free,
    COUNT(*) AS publication_count
FROM etl_publications
WHERE job_run = (
    SELECT MAX(job_run)
    FROM etl_publications
)
GROUP BY
    shipping_mode,
    shipping_logistic_type,
    shipping_free
ORDER BY publication_count DESC;
    """)

    print("Resultado:")

    for __row in __cursor.fetchall():
        print(__row)

if __name__ == "__main__":
    check_database()