import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()

# Variaveis globais
ML_DATABASE = os.getenv("ML_DATABASE")

# Conectar ao banco
def get_connection():
    """
    Cria uma conexão com o banco SQLite.
    """

    # TryCath
    try:

        __connection = sqlite3.connect(ML_DATABASE)
        return __connection

    # Exception
    except Exception as e:
        print(f"Erro ao criar a conexão no banco:\n{e}")
        return None