# Mercado Livre — Automação ETL

Projeto desenvolvido como solução para o desafio técnico de **Automação ETL com Python**, utilizando as APIs públicas do Mercado Livre.

O objetivo é extrair informações de produtos e publicações do Mercado Livre Argentina, transformar os dados e disponibilizá-los para análise das principais métricas solicitadas pelo desafio.

---

## Objetivo

O cenário proposto consiste em apoiar um vendedor do Mercado Livre Argentina interessado em analisar publicações de produtos **Samsung Galaxy**, considerando diferentes modelos.

A solução desenvolvida realiza um processo ETL (**Extract, Transform, Load**) para responder às seguintes perguntas de negócio:

1. Existe algum vendedor com múltiplas publicações? Quantas?
2. Qual a média de vendas por vendedor?
3. Qual o preço médio dos produtos em USD?
4. Qual o percentual de itens que possuem garantia?
5. Quais métodos de envio são oferecidos?

---

## Arquitetura

O projeto foi estruturado em três etapas principais:

```text
                    Mercado Livre API
                           │
                           ▼
                    ┌─────────────┐
                    │   EXTRACT   │
                    │             │
                    │ Products    │
                    │ Items       │
                    │ Currency    │
                    └──────┬──────┘
                           │
                           ▼
                    ┌─────────────┐
                    │  TRANSFORM  │
                    │             │
                    │ DataFrame   │
                    │ Price USD   │
                    │ Warranty    │
                    │ Shipping    │
                    └──────┬──────┘
                           │
                           ▼
                    ┌─────────────┐
                    │    LOAD     │
                    │             │
                    │   SQLite    │
                    └──────┬──────┘
                           │
                           ▼
                    ┌─────────────┐
                    │ SQL Queries │
                    │             │
                    │ Business    │
                    │ Questions   │
                    └─────────────┘
```

### Fluxo de dados

1. Renovação do token de acesso.
2. Busca dos produtos Samsung Galaxy ativos.
3. Filtragem pelo domínio de celulares.
4. Busca das publicações relacionadas a cada produto.
5. Filtragem de produtos novos.
6. Consulta dos detalhes das publicações.
7. Consulta da taxa de conversão ARS → USD.
8. Transformação dos dados em DataFrame.
9. Inclusão do identificador `JOB_RUN`.
10. Persistência dos dados no banco.
11. Execução das consultas SQL para responder às perguntas de negócio.

---

## Tecnologias utilizadas

* Python 3.12
* Requests
* Pandas
* python-dotenv
* SQLite
* SQL
* API REST do Mercado Livre

### Principais conceitos utilizados

* ETL
* API REST
* Paginação
* Variáveis de ambiente
* Tratamento de exceções
* Data transformation
* Persistência de dados
* SQL analítico

---

## Estrutura do projeto

```text
mercado-libre-automatizacion-etl/
│
├── src/
│   ├── api/
│   │   ├── client.py
│   │   ├── products.py
│   │   ├── items.py
│   │   └── currencies.py
│   │
│   ├── database/
│   │   ├── connection.py
│   │   ├── models.py
│   │   ├── load.py
│   │   └── transform.py
│   │
│   └── token/
│       └── auth.py
│
├── sql/
│   └── queries.sql
│
├── test/
│   └── db.py
│
├── .env
├── .gitignore
├── main.py
├── requirements.txt
├── README.md
└── mercado_livre.db
```

---

# Configuração

## 1. Clonar o projeto

```bash
git clone <URL_DO_REPOSITORIO>
cd mercado-libre-automatizacion-etl
```

---

## 2. Criar ambiente virtual

### Windows

```powershell
python -m venv .venv
```

Ativação:

```powershell
.venv\Scripts\Activate.ps1
```

---

## 3. Instalar dependências

```bash
pip install -r requirements.txt
```

---

## 4. Configurar variáveis de ambiente

Criar um arquivo `.env` na raiz do projeto.

Exemplo:

```env
ML_URL=https://api.mercadolibre.com

ML_PRODUCTS=products
ML_SEARCH=search
ML_ITEMS=items
ML_CURRENCY=currency_conversions

ML_SITE_ID=MLA
ML_SEARCH_QUERY=Samsung Galaxy
ML_SEARCH_DOMAIN=MLA-CELLPHONES
ML_SEARCH_PAGE_SIZE=50

ML_ACCESS_TOKEN=SEU_ACCESS_TOKEN
```

### Segurança

Credenciais e tokens não são armazenados diretamente no código-fonte.

O token é carregado através da variável:

```env
ML_ACCESS_TOKEN
```

---

# Execução

Após configurar o ambiente e as variáveis de ambiente:

```bash
python main.py
```

O processo realiza automaticamente:

```text
1. Criação das tabelas
2. Renovação do token
3. Extração dos produtos
4. Extração das publicações
5. Consulta dos detalhes dos itens
6. Consulta da conversão ARS → USD
7. Transformação dos dados
8. Inclusão do JOB_RUN
9. Carga no banco
```

Ao final:

```text
Dados carregados no banco com sucesso.
```

---

# Extração

## Busca de produtos

A API de produtos é utilizada para localizar produtos Samsung Galaxy ativos no Mercado Livre Argentina.

São utilizados parâmetros como:

```text
status = active
site_id = MLA
q = Samsung Galaxy
limit = 50
offset = 0
```

Também é aplicado o domínio:

```text
MLA-CELLPHONES
```

A API de produtos suporta a utilização de `q`, `site_id`, `status`, `domain_id`, `offset` e `limit` para a busca de produtos.

---

## Paginação

As consultas são realizadas utilizando páginas de até **50 registros**.

Exemplo:

```text
offset = 0
limit = 50

offset = 50
limit = 50

offset = 100
limit = 50
```

A paginação continua até que a API retorne uma quantidade de registros inferior ao limite configurado.

---

## Produtos novos

Após a busca das publicações, somente itens com:

```text
condition = new
```

são considerados no processo.

Dessa forma, produtos usados não participam das análises.

---

# Conversão de moeda

Os preços das publicações são originalmente retornados em ARS.

A aplicação consulta a API de conversão do Mercado Livre para obter a taxa:

```text
ARS → USD
```

A conversão é realizada através de:

```text
price_usd = price * currency_rate
```

Exemplo:

```text
Preço: ARS 1.000.000

Taxa: 0.00066313

Preço em USD:
1.000.000 × 0.00066313
= USD 663,13
```

A taxa utilizada na execução também é armazenada no banco.

---

# Transformação

Os dados extraídos são transformados em um `pandas.DataFrame`.

Durante essa etapa são tratados:

* preço;
* moeda;
* conversão para USD;
* garantia;
* informações de envio;
* condição do produto;
* vendedor;
* publicação;
* `JOB_RUN`.

### Garantia

O campo `warranty` é convertido para um indicador booleano:

```text
has_warranty
```

Publicações sem garantia, incluindo:

```text
Sin garantía
```

são consideradas como:

```text
has_warranty = false
```

---

# Banco de dados

## Banco utilizado

A implementação atual utiliza:

```text
SQLite
```

Arquivo:

```text
mercado_livre.db
```

A escolha foi feita para manter a execução local simples e facilitar a reprodução do desafio sem necessidade de infraestrutura adicional.

---

# Modelo de dados

Tabela:

```text
etl_publications
```

| Campo                    | Tipo     | Descrição                    |
| ------------------------ | -------- | ---------------------------- |
| `id`                     | INTEGER  | Identificador interno        |
| `job_run`                | DATETIME | Data/hora da execução do ETL |
| `product_id`             | TEXT     | ID do produto de catálogo    |
| `product_name`           | TEXT     | Nome do produto              |
| `item_id`                | TEXT     | ID da publicação             |
| `seller_id`              | INTEGER  | ID do vendedor               |
| `price`                  | REAL     | Preço original               |
| `currency_id`            | TEXT     | Moeda original               |
| `currency_rate`          | REAL     | Taxa de conversão utilizada  |
| `price_usd`              | REAL     | Preço convertido para USD    |
| `sold_quantity`          | INTEGER  | Quantidade vendida           |
| `condition`              | TEXT     | Condição do produto          |
| `warranty`               | TEXT     | Informação da garantia       |
| `has_warranty`           | BOOLEAN  | Indicador de garantia        |
| `listing_type_id`        | TEXT     | Tipo da publicação           |
| `shipping_mode`          | TEXT     | Modo de envio                |
| `shipping_logistic_type` | TEXT     | Tipo de logística            |
| `shipping_free`          | BOOLEAN  | Indicador de frete grátis    |

---

# JOB_RUN

Cada execução do ETL recebe um único timestamp:

```python
__job_run = datetime.now()
```

Esse mesmo valor é associado a todos os registros daquela execução.

Isso permite:

* identificar cada execução;
* manter histórico;
* comparar diferentes execuções;
* consultar somente o último processamento.

Exemplo:

```sql
WHERE job_run = (
    SELECT MAX(job_run)
    FROM etl_publications
)
```

---

# Perguntas de negócio

## Questão 1 — Vendedores com múltiplas publicações

### Query

```sql
SELECT seller_id, COUNT(*) AS publication_count
FROM etl_publications
WHERE job_run = (
    SELECT MAX(job_run)
    FROM etl_publications
)
GROUP BY seller_id
HAVING COUNT(*) > 1
ORDER BY publication_count DESC;
```

### Resultado

```text
seller_id    publication_count
214988544    2
```

### Conclusão

Existe vendedor com múltiplas publicações.

O vendedor:

```text
214988544
```

possui:

```text
2 publicações
```

---

# Questão 2 — Média de vendas por vendedor

### Query

```sql
SELECT seller_id, ROUND(AVG(sold_quantity), 2) AS average_sales
FROM etl_publications
WHERE job_run = (
    SELECT MAX(job_run)
    FROM etl_publications
)
AND sold_quantity IS NOT NULL
GROUP BY seller_id
ORDER BY average_sales DESC;
```

### Limitação encontrada

Durante a execução do desafio, as chamadas ao endpoint:

```text
/items/{ITEM_ID}
```

retornaram:

```text
HTTP 403
```

O endpoint de detalhes do item disponibiliza o campo `sold_quantity`, porém o acesso aos itens utilizados na execução não foi autorizado. A própria documentação do Mercado Livre orienta revisar erros `401` e `403` nas consultas de itens.

Por esse motivo:

* `sold_quantity` não foi preenchido artificialmente;
* valores ausentes são armazenados como `NULL`;
* registros sem esse dado não entram no cálculo da média.

Essa decisão evita interpretar ausência de informação como:

```text
sold_quantity = 0
```

e produzir uma análise incorreta.

---

# Questão 3 — Preço médio em USD

### Query

```sql
SELECT ROUND(AVG(price_usd), 2) AS average_price_usd
FROM etl_publications
WHERE job_run = (
    SELECT MAX(job_run)
    FROM etl_publications
)
AND price_usd IS NOT NULL;
```

### Resultado

```text
USD 1.067,88
```

Portanto, o preço médio das publicações analisadas foi de aproximadamente:

**US$ 1.067,88**

---

# Questão 4 — Percentual de itens com garantia

### Query

```sql
SELECT
    ROUND(
        100.0 * SUM(
            CASE
                WHEN has_warranty = 1 THEN 1
                ELSE 0
            END
        ) / COUNT(*),
        2
    ) AS warranty_percentage
FROM etl_publications
WHERE job_run = (
    SELECT MAX(job_run)
    FROM etl_publications
);
```

### Resultado

```text
81.25%
```

Portanto:

* **13 publicações** possuem garantia;
* **3 publicações** não possuem garantia;
* percentual com garantia: **81,25%**.

---

# Questão 5 — Métodos de envio

### Query

```sql
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
```

### Resultado

| Modo  | Tipo de logística | Frete grátis | Publicações |
| ----- | ----------------- | ------------ | ----------: |
| `me2` | `drop_off`        | Sim          |           7 |
| `me2` | `xd_drop_off`     | Sim          |           7 |
| `me2` | `cross_docking`   | Sim          |           2 |

Os dados de envio são obtidos a partir dos atributos da publicação, incluindo `shipping.mode`, `shipping.logistic_type` e `shipping.free_shipping`. A documentação do Mercado Livre apresenta esses campos no detalhe de um item.

---

# Resumo dos resultados

| Questão                            | Resultado                          |
| ---------------------------------- | ---------------------------------- |
| Vendedor com múltiplas publicações | Seller `214988544` — 2 publicações |
| Média de vendas por vendedor       | Indisponível devido ao HTTP 403    |
| Preço médio em USD                 | **US$ 1.067,88**                   |
| Publicações com garantia           | **81,25%**                         |
| `drop_off`                         | **7 publicações**                  |
| `xd_drop_off`                      | **7 publicações**                  |
| `cross_docking`                    | **2 publicações**                  |
| Frete grátis                       | **16 publicações**                 |

---

# Validação

A execução utilizada para os resultados apresentados produziu:

```text
Total de registros: 16
```

O histórico de execução também foi validado através do campo `JOB_RUN`.

Exemplo:

```text
2026-09-07 11:32:10.006614 → 16 registros
```

---

# Decisões técnicas

## Uso de funções separadas por responsabilidade

A aplicação foi dividida em módulos para evitar que toda a lógica fique concentrada em um único arquivo.

### API

Responsável pelas chamadas externas:

```text
src/api/
```

### Banco

Responsável pela conexão, modelo e carga:

```text
src/database/
```

### Token

Responsável pela renovação do token:

```text
src/token/
```

### SQL

Consultas analíticas separadas do código Python:

```text
sql/queries.sql
```

---

## Variáveis de ambiente

Credenciais e configurações sensíveis são mantidas fora do código-fonte.

Isso permite alterar:

* token;
* URL;
* endpoints;
* parâmetros de busca;
* tamanho da paginação;

sem modificar o código.

---

## Tratamento de erros

As chamadas à API possuem tratamento de exceções e timeout.

Exemplo:

```python
response = requests.get(
    url,
    headers=get_headers(),
    params=params,
    timeout=15,
)
```

Erros HTTP são propagados através de:

```python
response.raise_for_status()
```

e tratados nas funções de extração.

---

# Limitações conhecidas

## `sold_quantity`

O endpoint `/items/{ITEM_ID}` retornou HTTP 403 durante a execução.

Consequentemente, a quantidade vendida não pôde ser obtida para os registros analisados.

A aplicação mantém o campo no modelo como `NULL` quando o dado não está disponível, evitando a criação de dados fictícios.

---

## Busca de itens

Também foi testado o endpoint de busca de itens `/sites/$SITE_ID/search`, conforme apresentado na documentação de Busca de itens do Mercado Livre.

Durante a execução, as requisições para esse endpoint também retornaram HTTP 403 (Forbidden).

Dessa forma, o endpoint não foi utilizado como fonte de dados na implementação final.

Foi observada uma possível divergência entre o comportamento atual da API e o endpoint apresentado na documentação consultada, o que pode indicar que a documentação disponível não esteja totalmente alinhada com as permissões ou com a versão atualmente disponibilizada da API.

Essa limitação foi considerada na implementação e não foram utilizados dados estimados ou simulados para contorná-la.

---

## Banco de dados

A implementação atual utiliza SQLite pela simplicidade de execução local.

---

# Referências

* [Mercado Livre Developers — API Docs](https://developers.mercadolivre.com.br/pt_br/api-docs?utm_source=chatgpt.com)
* [Mercado Livre Developers — Buscador de produtos](https://developers.mercadolivre.com.br/buscador-de-produtos?utm_source=chatgpt.com)
* [Mercado Livre Developers — Busca de itens](https://developers.mercadolivre.com.br/pt_br/convivencia-me1-me2/itens-e-buscas?utm_source=chatgpt.com)
* [Mercado Livre Developers — Mercado Envios](https://developers.mercadolivre.com.br/pt_br/mercado-envios?utm_source=chatgpt.com)

---

# Autor

**Brenno Brossi**

Projeto desenvolvido para avaliação técnica de Automação ETL com Python.
