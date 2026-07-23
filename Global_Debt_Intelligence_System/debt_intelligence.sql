
CREATE DATABASE IF NOT EXISTS global_debt_intelligence;
USE global_debt_intelligence;

--------------------------------------------------
-- COUNTRIES
--------------------------------------------------

CREATE TABLE Countries(
    country_id INT AUTO_INCREMENT PRIMARY KEY,
    country_name VARCHAR(100),
    region VARCHAR(100),
    population BIGINT
);

--------------------------------------------------
-- DEBT INDICATORS
--------------------------------------------------

CREATE TABLE DebtIndicators(
    indicator_id INT AUTO_INCREMENT PRIMARY KEY,
    indicator_name VARCHAR(255)
);

--------------------------------------------------
-- COUNTRY DEBT
--------------------------------------------------

CREATE TABLE CountryDebt(
    debt_id INT AUTO_INCREMENT PRIMARY KEY,

    country_id INT,
    indicator_id INT,

    debt_year INT,

    debt_amount DECIMAL(18,2),

    forgiven_amount DECIMAL(18,2),

    FOREIGN KEY(country_id)
    REFERENCES Countries(country_id),

    FOREIGN KEY(indicator_id)
    REFERENCES DebtIndicators(indicator_id)
);

--------------------------------------------------
-- SAMPLE COUNTRIES
--------------------------------------------------

INSERT INTO Countries
(country_name, region, population)
VALUES
('Brazil','South America',214000000),
('India','Asia',1400000000),
('Mexico','North America',130000000),
('Indonesia','Asia',275000000),
('Nigeria','Africa',223000000),
('Colombia','South America',52000000),
('Argentina','South America',46000000),
('Pakistan','Asia',240000000);

--------------------------------------------------
-- SAMPLE INDICATORS
--------------------------------------------------

INSERT INTO DebtIndicators(indicator_name)
VALUES
('Long-Term External Debt'),
('Short-Term External Debt'),
('Multilateral Debt'),
('Bilateral Debt'),
('Private Debt');

--------------------------------------------------
-- SAMPLE DEBT
--------------------------------------------------

INSERT INTO CountryDebt
(country_id,indicator_id,debt_year,debt_amount,forgiven_amount)
VALUES
(1,1,2024,12000000000,50000000),
(2,1,2024,25000000000,120000000),
(3,2,2024,7000000000,10000000),
(4,3,2024,9000000000,25000000),
(5,1,2024,15000000000,5000000),
(6,4,2024,4000000000,3000000),
(7,2,2024,6500000000,8000000),
(8,3,2024,10000000000,20000000);

--------------------------------------------------
-- QUERIES
--------------------------------------------------

-- Total Global Debt

SELECT
SUM(debt_amount) AS global_debt
FROM CountryDebt;

--------------------------------------------------

-- Most Indebted Countries

SELECT
c.country_name,
SUM(cd.debt_amount) total_debt

FROM CountryDebt cd
JOIN Countries c
ON cd.country_id=c.country_id

GROUP BY c.country_name

ORDER BY total_debt DESC;

--------------------------------------------------

-- Debt by Region

SELECT
c.region,
SUM(cd.debt_amount) total_debt

FROM CountryDebt cd
JOIN Countries c
ON cd.country_id=c.country_id

GROUP BY c.region

ORDER BY total_debt DESC;

--------------------------------------------------

-- Debt Forgiveness

SELECT
c.country_name,
SUM(cd.forgiven_amount) forgiven

FROM CountryDebt cd
JOIN Countries c
ON cd.country_id=c.country_id

GROUP BY c.country_name

ORDER BY forgiven DESC;

--------------------------------------------------

-- Average Debt

SELECT
AVG(country_total_debt)

FROM(

SELECT
country_id,
SUM(debt_amount) country_total_debt

FROM CountryDebt

GROUP BY country_id

)t;

--------------------------------------------------

-- Debt Structure

SELECT
di.indicator_name,
SUM(cd.debt_amount) total

FROM CountryDebt cd
JOIN DebtIndicators di
ON cd.indicator_id=di.indicator_id

GROUP BY di.indicator_name

ORDER BY total DESC;

--------------------------------------------------

-- Debt Per Capita

SELECT
c.country_name,

ROUND(
SUM(cd.debt_amount)/c.population,
2
) debt_per_capita

FROM CountryDebt cd
JOIN Countries c
ON cd.country_id=c.country_id

GROUP BY c.country_name,c.population

ORDER BY debt_per_capita DESC;