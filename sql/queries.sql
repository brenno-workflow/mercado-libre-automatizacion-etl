-- QUESTÃO 1
-- Vendedores com múltiplas publicações
-- Vendedor con múltiples publicaciones

SELECT seller_id, COUNT(*) AS publication_count
FROM etl_publications
WHERE job_run = (
    SELECT MAX(job_run)
    FROM etl_publications
)
GROUP BY seller_id
HAVING COUNT(*) > 1
ORDER BY publication_count DESC;

-- QUESTÃO 2
-- Média de vendas por vendedor
-- Promedio de ventas por seller?

SELECT seller_id, ROUND(AVG(sold_quantity), 2) AS average_sales
FROM etl_publications
WHERE job_run = (
    SELECT MAX(job_run)
    FROM etl_publications
)
AND sold_quantity IS NOT NULL
GROUP BY seller_id
ORDER BY average_sales DESC;

-- QUESTÃO 3
-- Preço médio das publicações em USD
-- Precio promedio en dólares

SELECT ROUND(AVG(price_usd), 2) AS average_price_usd
FROM etl_publications
WHERE job_run = (
    SELECT MAX(job_run)
    FROM etl_publications
)
AND price_usd IS NOT NULL;

-- QUESTÃO 4
-- Percentual de itens com garantia
-- Porcentaje de artículos con garantía

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

-- QUESTÃO 5
-- Métodos de envio oferecidos
-- Métodos de Shipping que ofrecen

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
