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
print(f"==================================================")
print(f"🚀 Iniciando ETL Autenticado Job Run: {job_run_time}")
print(f"==================================================\n")

if not TOKEN:
    print("❌ Erro: ML_ACCESS_TOKEN não foi encontrado no arquivo .env!")
    exit()

# Configuração dos cabeçalhos oficiais com o seu Token Bearer
headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/json",
    "User-Agent": "Mozilla/5.0"
}

# 2. Obter taxa de câmbio real
def obter_taxa_cambio():
    url = f"{BASE_URL}/currency_conversions/search?from=ARS&to=USD"
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json().get("ratio", 0.001)
    except Exception as e:
        print(f"⚠️ Erro ao buscar câmbio ({e}).")
    print("⚠️ Usando taxa estável de fallback para ARS -> USD.")
    return 0.00105 

# 3. Processo Principal de Extração Autenticada
def executar_etl_autenticado():
    taxa_usd = obter_taxa_cambio()
    print(f"📊 Taxa ARS -> USD aplicada: {taxa_usd}")
    
    # URL oficial de busca com filtro de novos e limite exigidos (Requisitos 2 e 3)
    #url_busca = f"https://api.mercadolibre.com/products/MLB2000024021"
    url_busca = f"https://api.mercadolibre.com/products/search?status=active&q=Samsung%20Galaxy&site_id=MLA"
    url_busca = f"https://api.mercadolibre.com/products/search?status=active&q=Samsung%20Galaxy&site_id=MLA"
    
    print(f"📡 Conectando à API real do Mercado Livre com Access Token...")
    response = requests.get(url_busca, headers=headers, timeout=15)
    
    if response.status_code != 200:
        print(f"❌ Falha na autenticação ou requisição. Status: {response.status_code}")
        print(response.text[:300])
        return []

    print("✅ Autenticação bem-sucedida! Dados extraídos em tempo real.")
    data_json = response.json()
    print(data_json)
    resultados = data_json.get("results", [])
    
    dados_processados = []
    for prod in resultados:
        preco_ars = prod.get("price", 0)
        preco_usd = preco_ars * taxa_usd
        
        # Mapeamento do método de envio
        shipping_mode = prod.get("shipping", {}).get("mode", "not_specified")
        
        # Verificação básica de garantia nos atributos/termos da busca
        has_warranty = "Não"
        sale_terms = prod.get("sale_terms", [])
        for term in sale_terms:
            if "warranty" in term.get("id", "").lower():
                has_warranty = "Sim"
                break
                
        item_estruturado = {
            "JOB_RUN": job_run_time,
            "ITEM_ID": prod.get("id"),
            "TITLE": prod.get("title"),
            "SELLER_ID": prod.get("seller", {}).get("id"),
            "PRICE_ARS": preco_ars,
            "PRICE_USD": round(preco_usd, 2),
            "SOLD_QUANTITY": prod.get("sold_quantity", 0) or 0,
            "HAS_WARRANTY": has_warranty,
            "SHIPPING_METHOD": shipping_mode
        }
        dados_processados.append(item_estruturado)
        
    return dados_processados

# Executar e exibir resultado real
dados_reais = executar_etl_autenticado()

if dados_reais:
    print(f"\n==================================================")
    print(f"🎉 ETL Concluído com Sucesso! {len(dados_reais)} registros REAIS extraídos.")
    print(f"==================================================")
    print(json.dumps(dados_reais[:2], indent=4, ensure_ascii=False))