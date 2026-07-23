
CREATE DATABASE IF NOT EXISTS sales_analysis;
USE sales_analysis;

--------------------------------------------------
-- STORES
--------------------------------------------------

CREATE TABLE Stores(
    store_id INT AUTO_INCREMENT PRIMARY KEY,
    store_name VARCHAR(150),
    city VARCHAR(100)
);

--------------------------------------------------
-- CUSTOMERS
--------------------------------------------------

CREATE TABLE Customers(
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_name VARCHAR(150),
    city VARCHAR(100)
);

--------------------------------------------------
-- CATEGORIES
--------------------------------------------------

CREATE TABLE Categories(
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(100)
);

--------------------------------------------------
-- PRODUCTS
--------------------------------------------------

CREATE TABLE Products(
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    product_name VARCHAR(150),
    category_id INT,
    price DECIMAL(10,2),

    FOREIGN KEY(category_id)
    REFERENCES Categories(category_id)
);

--------------------------------------------------
-- SALES
--------------------------------------------------

CREATE TABLE Sales(
    sale_id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT,
    customer_id INT,
    store_id INT,

    quantity INT,
    payment_method VARCHAR(50),
    sale_date DATE,

    FOREIGN KEY(product_id)
    REFERENCES Products(product_id),

    FOREIGN KEY(customer_id)
    REFERENCES Customers(customer_id),

    FOREIGN KEY(store_id)
    REFERENCES Stores(store_id)
);

--------------------------------------------------
-- SAMPLE DATA
--------------------------------------------------

INSERT INTO Categories(category_name)
VALUES
('Beverages'),
('Dairy'),
('Snacks'),
('Fruits'),
('Vegetables');

INSERT INTO Stores(store_name,city)
VALUES
('Store North','Bogota'),
('Store South','Medellin'),
('Store West','Cali');

--------------------------------------------------
-- QUERIES
--------------------------------------------------

-- Sales by category

SELECT
c.category_name,
SUM(s.quantity * p.price) revenue
FROM Sales s
JOIN Products p
ON s.product_id=p.product_id
JOIN Categories c
ON p.category_id=c.category_id
GROUP BY c.category_name
ORDER BY revenue DESC;

-- Sales by location

SELECT
st.city,
SUM(s.quantity * p.price) revenue
FROM Sales s
JOIN Products p
ON s.product_id=p.product_id
JOIN Stores st
ON s.store_id=st.store_id
GROUP BY st.city
ORDER BY revenue DESC;

-- Payment methods

SELECT
payment_method,
COUNT(*) transactions
FROM Sales
GROUP BY payment_method
ORDER BY transactions DESC;

-- Top products

SELECT
p.product_name,
SUM(quantity) units_sold
FROM Sales s
JOIN Products p
ON s.product_id=p.product_id
GROUP BY p.product_name
ORDER BY units_sold DESC
LIMIT 10;

-- Monthly sales

SELECT
YEAR(sale_date) year,
MONTH(sale_date) month,
SUM(quantity*p.price) revenue
FROM Sales s
JOIN Products p
ON s.product_id=p.product_id
GROUP BY year,month
ORDER BY year,month;

-- Average transaction

SELECT
AVG(quantity*p.price) avg_transaction
FROM Sales s
JOIN Products p
ON s.product_id=p.product_id;

-- Best performing store

SELECT
st.store_name,
SUM(quantity*p.price) revenue
FROM Sales s
JOIN Products p
ON s.product_id=p.product_id
JOIN Stores st
ON s.store_id=st.store_id
GROUP BY st.store_name
ORDER BY revenue DESC;