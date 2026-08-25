-- Считает общее количество покупателей в таблице customers
SELECT count(*) AS customers_count FROM customers;

-- Топ-10 продавцов по суммарной выручке: продавец, количество сделок, выручка
SELECT
    CONCAT(e.first_name, ' ', e.last_name) AS seller,
    COUNT(*) AS operations,
    FLOOR(SUM(s.quantity * p.price)) AS income
FROM sales s
JOIN employees e ON e.employee_id = s.sales_person_id
JOIN products p ON p.product_id = s.product_id
GROUP BY e.employee_id, e.first_name, e.last_name
ORDER BY income DESC
LIMIT 10;

-- Продавцы, чья средняя выручка за сделку ниже средней выручки за сделку по всем продажам
WITH per_seller AS (
    SELECT
        e.employee_id,
        CONCAT(e.first_name, ' ', e.last_name) AS seller,
        FLOOR(AVG(s.quantity * p.price)) AS average_income
    FROM sales s
    JOIN employees e ON e.employee_id = s.sales_person_id
    JOIN products p ON p.product_id = s.product_id
    GROUP BY e.employee_id, e.first_name, e.last_name
),
overall AS (
    SELECT AVG(s.quantity * p.price) AS overall_avg
    FROM sales s
    JOIN products p ON p.product_id = s.product_id
)
SELECT seller, average_income
FROM per_seller, overall
WHERE average_income < overall_avg
ORDER BY average_income ASC;

-- Выручка каждого продавца по дням недели, отсортированная по номеру дня недели и продавцу
SELECT
    CONCAT(e.first_name, ' ', e.last_name) AS seller,
    TRIM(TO_CHAR(s.sale_date, 'day')) AS day_of_week,
    FLOOR(SUM(s.quantity * p.price)) AS income
FROM sales s
JOIN employees e ON e.employee_id = s.sales_person_id
JOIN products p ON p.product_id = s.product_id
GROUP BY e.employee_id, e.first_name, e.last_name, EXTRACT(ISODOW FROM s.sale_date), TRIM(TO_CHAR(s.sale_date, 'day'))
ORDER BY EXTRACT(ISODOW FROM s.sale_date), seller;

-- Количество покупателей по возрастным группам: 16-25, 26-40, 40+
SELECT age_category, COUNT(*) AS age_count
FROM (
    SELECT
        CASE
            WHEN age BETWEEN 16 AND 25 THEN '16-25'
            WHEN age BETWEEN 26 AND 40 THEN '26-40'
            ELSE '40+'
        END AS age_category
    FROM customers
) t
GROUP BY age_category
ORDER BY age_category;

-- Количество уникальных покупателей и выручка по месяцам (ГОД-МЕСЯЦ)
SELECT
    TO_CHAR(s.sale_date, 'YYYY-MM') AS selling_month,
    COUNT(DISTINCT s.customer_id) AS total_customers,
    FLOOR(SUM(s.quantity * p.price)) AS income
FROM sales s
JOIN products p ON p.product_id = s.product_id
GROUP BY TO_CHAR(s.sale_date, 'YYYY-MM')
ORDER BY selling_month ASC;

-- Покупатели, чья первая покупка пришлась на акционный товар (цена = 0)
WITH first_purchase AS (
    SELECT
        s.*,
        ROW_NUMBER() OVER (PARTITION BY s.customer_id ORDER BY s.sale_date, s.sales_id) AS rn
    FROM sales s
)
SELECT
    CONCAT(c.first_name, ' ', c.last_name) AS customer,
    fp.sale_date,
    CONCAT(e.first_name, ' ', e.last_name) AS seller
FROM first_purchase fp
JOIN products p ON p.product_id = fp.product_id
JOIN customers c ON c.customer_id = fp.customer_id
JOIN employees e ON e.employee_id = fp.sales_person_id
WHERE fp.rn = 1 AND p.price = 0
ORDER BY fp.customer_id;
