
-- project_queries.sql
DROP TABLE IF EXISTS customer_value;
CREATE TABLE customer_value (
    customer TEXT PRIMARY KEY,
    state TEXT,
    customer_lifetime_value REAL,
    response TEXT,
    coverage TEXT,
    education TEXT,
    effective_to_date TEXT,
    employmentstatus TEXT,
    gender TEXT,
    income REAL,
    location_code TEXT,
    marital_status TEXT,
    monthly_premium_auto REAL,
    months_since_last_claim INTEGER,
    months_since_policy_inception INTEGER,
    number_of_open_complaints INTEGER,
    number_of_policies INTEGER,
    policy_type TEXT,
    policy TEXT,
    renew_offer_type TEXT,
    sales_channel TEXT,
    total_claim_amount REAL,
    vehicle_class TEXT,
    vehicle_size TEXT
);

-- Q1.
SELECT state, coverage, AVG(customer_lifetime_value) AS avg_clv
FROM customer_value
GROUP BY state, coverage
ORDER BY avg_clv DESC;

-- Q2.
SELECT education,
       COUNT(*) AS total,
       SUM(CASE WHEN response = 'Yes' THEN 1 ELSE 0 END) AS responded,
       ROUND(100.0 * SUM(CASE WHEN response = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS response_rate
FROM customer_value
GROUP BY education
ORDER BY response_rate DESC;

-- Q3.
SELECT CASE
         WHEN income < 30000 THEN '<30k'
         WHEN income BETWEEN 30000 AND 60000 THEN '30k-60k'
         WHEN income BETWEEN 60001 AND 90000 THEN '60k-90k'
         ELSE '>90k'
       END AS income_range,
       AVG(customer_lifetime_value) AS avg_clv,
       COUNT(*) AS num_customers
FROM customer_value
WHERE income > 0
GROUP BY income_range
ORDER BY income_range;

-- Q4.
SELECT customer, state, customer_lifetime_value, income, response
FROM customer_value
ORDER BY customer_lifetime_value DESC
LIMIT 10;

-- Q5.
SELECT number_of_open_complaints,
       AVG(customer_lifetime_value) AS avg_clv,
       COUNT(*) AS count
FROM customer_value
GROUP BY number_of_open_complaints
ORDER BY number_of_open_complaints;

-- Q6.
SELECT policy_type, 
       COUNT(*) AS total,
       SUM(CASE WHEN response = 'Yes' THEN 1 ELSE 0 END) AS responders
FROM customer_value
GROUP BY policy_type
ORDER BY responders DESC;