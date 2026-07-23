
CREATE DATABASE IF NOT EXISTS retail_revenue_hub;
USE retail_revenue_hub;

--------------------------------------------------
-- SALES TABLE
--------------------------------------------------

CREATE TABLE SalesData(

ORDERNUMBER INT,

QUANTITYORDERED INT,

PRICEEACH DECIMAL(10,2),

ORDERLINENUMBER INT,

SALES DECIMAL(12,2),

ORDERDATE DATE,

STATUS VARCHAR(50),

QTR_ID INT,

MONTH_ID INT,

YEAR_ID INT,

PRODUCTLINE VARCHAR(100),

MSRP DECIMAL(10,2),

PRODUCTCODE VARCHAR(50),

CUSTOMERNAME VARCHAR(150),

PHONE VARCHAR(100),

ADDRESSLINE1 VARCHAR(255),

CITY VARCHAR(100),

STATE VARCHAR(100),

COUNTRY VARCHAR(100),

TERRITORY VARCHAR(100),

CONTACTLASTNAME VARCHAR(100),

CONTACTFIRSTNAME VARCHAR(100),

DEALSIZE VARCHAR(50)

);

--------------------------------------------------
-- TOTAL REVENUE
--------------------------------------------------

SELECT
ROUND(SUM(SALES),2) total_revenue
FROM SalesData;

--------------------------------------------------
-- MONTHLY REVENUE
--------------------------------------------------

SELECT
YEAR_ID,
MONTH_ID,
SUM(SALES) revenue

FROM SalesData

GROUP BY YEAR_ID,MONTH_ID

ORDER BY YEAR_ID,MONTH_ID;

--------------------------------------------------
-- TOP CUSTOMERS
--------------------------------------------------

SELECT

CUSTOMERNAME,

SUM(SALES) revenue

FROM SalesData

GROUP BY CUSTOMERNAME

ORDER BY revenue DESC

LIMIT 20;

--------------------------------------------------
-- PRODUCT LINE PERFORMANCE
--------------------------------------------------

SELECT

PRODUCTLINE,

SUM(SALES) revenue

FROM SalesData

GROUP BY PRODUCTLINE

ORDER BY revenue DESC;

--------------------------------------------------
-- COUNTRY SALES
--------------------------------------------------

SELECT

COUNTRY,

SUM(SALES) revenue

FROM SalesData

GROUP BY COUNTRY

ORDER BY revenue DESC;

--------------------------------------------------
-- DEAL SIZE PERFORMANCE
--------------------------------------------------

SELECT

DEALSIZE,

SUM(SALES) revenue

FROM SalesData

GROUP BY DEALSIZE

ORDER BY revenue DESC;

--------------------------------------------------
-- BEST YEAR
--------------------------------------------------

SELECT

YEAR_ID,

SUM(SALES) revenue

FROM SalesData

GROUP BY YEAR_ID

ORDER BY revenue DESC;

--------------------------------------------------
-- ORDER STATUS
--------------------------------------------------

SELECT

STATUS,

COUNT(*) orders_count

FROM SalesData

GROUP BY STATUS;