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
