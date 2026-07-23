
CREATE DATABASE IF NOT EXISTS olist_customer_geography;
USE olist_customer_geography;

--------------------------------------------------
-- CUSTOMERS
--------------------------------------------------

CREATE TABLE OlistCustomers(

    customer_id VARCHAR(100),

    customer_unique_id VARCHAR(100),

    customer_zip_code_prefix INT,

    customer_city VARCHAR(100),

    customer_state VARCHAR(10)

);

--------------------------------------------------
-- TOTAL CUSTOMERS
--------------------------------------------------

SELECT
COUNT(*) total_customers
FROM OlistCustomers;

--------------------------------------------------
-- UNIQUE CUSTOMERS
--------------------------------------------------

SELECT
COUNT(DISTINCT customer_unique_id)
AS unique_customers
FROM OlistCustomers;

--------------------------------------------------
-- CUSTOMERS BY STATE
--------------------------------------------------

SELECT

customer_state,

COUNT(*) total_customers

FROM OlistCustomers

GROUP BY customer_state

ORDER BY total_customers DESC;

--------------------------------------------------
-- TOP 20 CITIES
--------------------------------------------------

SELECT

customer_city,

COUNT(*) total_customers

FROM OlistCustomers

GROUP BY customer_city

ORDER BY total_customers DESC

LIMIT 20;

--------------------------------------------------
-- ZIP CODE DISTRIBUTION
--------------------------------------------------

SELECT

customer_zip_code_prefix,

COUNT(*) total

FROM OlistCustomers

GROUP BY customer_zip_code_prefix

ORDER BY total DESC

LIMIT 20;

--------------------------------------------------
-- STATES WITH MOST UNIQUE CUSTOMERS
--------------------------------------------------

SELECT

customer_state,

COUNT(
DISTINCT customer_unique_id
) unique_customers

FROM OlistCustomers

GROUP BY customer_state

ORDER BY unique_customers DESC;

--------------------------------------------------
-- CUSTOMER CONCENTRATION
--------------------------------------------------

SELECT

customer_state,

ROUND(
100*COUNT(*)/
(
SELECT COUNT(*)
FROM OlistCustomers
),
2
) percentage

FROM OlistCustomers

GROUP BY customer_state

ORDER BY percentage DESC;

--------------------------------------------------
-- NUMBER OF CITIES SERVED
--------------------------------------------------

SELECT

COUNT(
DISTINCT customer_city
) total_cities

FROM OlistCustomers;