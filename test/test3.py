import os
import requests
import datetime
import json
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env (Requisito 8)
load_dotenv()
TOKEN = os.getenv("ML_ACCESS_TOKEN")

BASE_URL = "https://api.mercadolibre.com"

# 1. Busca produtos Samsung Galaxy
url = (
    f"{BASE_URL}/products/search"
    "?status=active"
    "&q=Samsung%20Galaxy"
    "&site_id=MLA"
    "&limit=50"
)

# Configuração dos cabeçalhos oficiais com o seu Token Bearer
headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/json",
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers, timeout=15)
response.raise_for_status()

products = response.json()["results"]

print(f"Produtos encontrados: {len(products)}")

# 2. Testa as publicações de cada produto
for product in products:

    product_id = product["id"]
    domain_id = product.get("domain_id")
    name = product.get("name")

    if domain_id != "MLA-CELLPHONES":
        continue

    url_items = f"{BASE_URL}/products/{product_id}/items"

    response = requests.get(url_items, headers=headers, timeout=15)

    print(
        f"{product_id} | "
        f"{response.status_code} | "
        f"{name}"
    )

    if response.status_code == 200:

        data = response.json()
        results = data.get("results", [])

        if results:
            print("\n" + "=" * 60)
            print(f"Produto: {product_id}")
            print(f"Nome: {product.get('name')}")
            print(f"Publicações: {len(results)}")

            for item in results:
                print(
                    f"  Item: {item.get('item_id')} | "
                    f"Seller: {item.get('seller_id')} | "
                    f"Preço: {item.get('price')} "
                    f"{item.get('currency_id')} | "
                    f"Condição: {item.get('condition')}"
                )