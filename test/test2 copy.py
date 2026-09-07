import os
import requests
import datetime
import json
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env (Requisito 8)
load_dotenv()
TOKEN = os.getenv("ML_ACCESS_TOKEN")

# 1. Configurações estruturadas (Requisito 7)
BASE_URL = "https://api.mercadolibre.com"
SITE_ID = "MLA"  # Argentina
SEARCH_TERM = "Samsung Galaxy"
PAGE_LIMIT = 50

# Definindo o JOB_RUN único para a corrida (Requisito 5)
job_run_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Configuração dos cabeçalhos oficiais com o seu Token Bearer
headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/json",
    "User-Agent": "Mozilla/5.0"
}

# 3. Processo Principal de Extração Autenticada
def executar_etl_autenticado():
    
    # URL oficial de busca com filtro de novos e limite exigidos (Requisitos 2 e 3)
    #url_busca = f"https://api.mercadolibre.com/products/MLB2000024021"
    #url_busca = f"https://api.mercadolibre.com/products/search?status=active&q=Samsung%20Galaxy&site_id=MLA"
    #url_busca = f"https://api.mercadolibre.com/products/MLA37965371"
    #url_busca = "https://api.mercadolibre.com/products/search?status=active&q=Samsung%20Galaxy&site_id=MLA"
    #url_busca = "https://api.mercadolibre.com/products/MLA37967802/items"
    url_busca = "https://api.mercadolibre.com/products/MLA37967802/items"

    response = requests.get(url_busca, headers=headers, timeout=15)
    print(response.json())

    BASE_URL = "https://api.mercadolibre.com"

    product_ids = [
        "MLA6002431",
        "MLA37967802",
        "MLA37965371",
        "MLA37980717",
    ]

    for product_id in product_ids:
        url = f"{BASE_URL}/products/{product_id}/items"

        response = requests.get(url, headers=headers)

        print(f"\n{product_id} -> {response.status_code}")

        if response.ok:
            data = response.json()
            print("Publicações:", len(data.get("results", [])))
        else:
            print(response.json().get("message"))
    
    

# Executar e exibir resultado real
dados_reais = executar_etl_autenticado()