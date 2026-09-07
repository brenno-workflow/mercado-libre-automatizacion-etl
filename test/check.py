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

    # Total de registros
    __cursor.execute(
        """
        SELECT COUNT(*)
        FROM etl_publications
        """
    )

    __total = __cursor.fetchone()[0]
    print(f"Total de registros: {__total}")

    # Registros por execução
    __cursor.execute(
        """
        SELECT job_run, COUNT(*)
        FROM etl_publications
        GROUP BY job_run
        ORDER BY job_run DESC
        """
    )

    print("\nRegistros por execução:")

    # Fet
    for __row in __cursor.fetchall():
        print(__row)

    __connection.close()

if __name__ == "__main__":
    check_database()