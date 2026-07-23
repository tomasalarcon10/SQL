
CREATE DATABASE IF NOT EXISTS smart_electricity;
USE smart_electricity;

--------------------------------------------------
-- CUSTOMERS
--------------------------------------------------

CREATE TABLE Customers(

    customer_id INT PRIMARY KEY,
    customer_name VARCHAR(100),

    city VARCHAR(100),
    state VARCHAR(100)

);

--------------------------------------------------
-- VENDORS
--------------------------------------------------

CREATE TABLE Vendors(

    vendor_id INT PRIMARY KEY,

    vendor_name VARCHAR(150)

);

--------------------------------------------------
-- ACCOUNTS
--------------------------------------------------

CREATE TABLE Accounts(

    account_id INT PRIMARY KEY,

    customer_id INT,

    account_number VARCHAR(50),

    FOREIGN KEY(customer_id)
    REFERENCES Customers(customer_id)

);

--------------------------------------------------
-- TARIFFS
--------------------------------------------------

CREATE TABLE Tariffs(

    tariff_id INT PRIMARY KEY,

    tariff_name VARCHAR(100),

    rate_per_unit DECIMAL(10,2)

);

--------------------------------------------------
-- CONSUMPTION
--------------------------------------------------

CREATE TABLE Consumption(

    meter_number VARCHAR(20) PRIMARY KEY,

    account_id INT,

    monthly_units INT,

    FOREIGN KEY(account_id)
    REFERENCES Accounts(account_id)

);

--------------------------------------------------
-- INVOICES
--------------------------------------------------

CREATE TABLE Invoices(

    invoice_id INT PRIMARY KEY,

    vendor_id INT,

    tariff_id INT,

    meter_number VARCHAR(20),

    invoice_date DATE,

    total_amount DECIMAL(12,2),

    FOREIGN KEY(vendor_id)
    REFERENCES Vendors(vendor_id),

    FOREIGN KEY(tariff_id)
    REFERENCES Tariffs(tariff_id),

    FOREIGN KEY(meter_number)
    REFERENCES Consumption(meter_number)

);

--------------------------------------------------
-- COMPLAINTS
--------------------------------------------------

CREATE TABLE Complaints(

    complaint_id INT AUTO_INCREMENT PRIMARY KEY,

    customer_id INT,

    complaint_type VARCHAR(100),

    complaint_status VARCHAR(50),

    created_date DATE,

    FOREIGN KEY(customer_id)
    REFERENCES Customers(customer_id)

);

--------------------------------------------------
-- BUSINESS QUERIES
--------------------------------------------------

-- Top consumers

SELECT
c.customer_name,
SUM(cons.monthly_units) units
FROM Customers c
JOIN Accounts a
ON c.customer_id=a.customer_id
JOIN Consumption cons
ON a.account_id=cons.account_id
GROUP BY c.customer_name
ORDER BY units DESC;

--------------------------------------------------

-- Revenue by vendor

SELECT
v.vendor_name,
SUM(i.total_amount) revenue

FROM Invoices i
JOIN Vendors v
ON i.vendor_id=v.vendor_id

GROUP BY v.vendor_name
ORDER BY revenue DESC;

--------------------------------------------------

-- Most common complaint

SELECT
complaint_type,
COUNT(*) total

FROM Complaints

GROUP BY complaint_type

ORDER BY total DESC;

--------------------------------------------------

-- Tariff performance

SELECT
t.tariff_name,
AVG(i.total_amount) avg_bill

FROM Invoices i
JOIN Tariffs t
ON i.tariff_id=t.tariff_id

GROUP BY t.tariff_name;

--------------------------------------------------

-- Average electricity usage

SELECT
AVG(monthly_units)
FROM Consumption;

--------------------------------------------------

-- Cities with highest usage

SELECT
c.city,
SUM(cons.monthly_units) total_units

FROM Customers c
JOIN Accounts a
ON c.customer_id=a.customer_id
JOIN Consumption cons
ON a.account_id=cons.account_id

GROUP BY c.city
ORDER BY total_units DESC;