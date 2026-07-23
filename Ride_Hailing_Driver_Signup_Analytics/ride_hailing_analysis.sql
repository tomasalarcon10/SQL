
CREATE DATABASE IF NOT EXISTS ride_hailing_analysis;
USE ride_hailing_analysis;

--------------------------------------------------
-- DRIVERS
--------------------------------------------------

CREATE TABLE Drivers(
    driver_id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(150),
    age INT,
    city VARCHAR(100),
    signup_date DATE
);

--------------------------------------------------
-- VERIFICATION
--------------------------------------------------

CREATE TABLE Verification(
    verification_id INT AUTO_INCREMENT PRIMARY KEY,
    driver_id INT,

    documents_submitted BOOLEAN,
    background_check BOOLEAN,
    verified BOOLEAN,

    FOREIGN KEY(driver_id)
    REFERENCES Drivers(driver_id)
);

--------------------------------------------------
-- INCENTIVES
--------------------------------------------------

CREATE TABLE Incentives(
    incentive_id INT AUTO_INCREMENT PRIMARY KEY,
    driver_id INT,

    incentive_type VARCHAR(100),
    incentive_amount DECIMAL(10,2),

    FOREIGN KEY(driver_id)
    REFERENCES Drivers(driver_id)
);

--------------------------------------------------
-- TRIPS
--------------------------------------------------

CREATE TABLE Trips(
    trip_id INT AUTO_INCREMENT PRIMARY KEY,
    driver_id INT,

    trip_date DATE,
    earnings DECIMAL(10,2),

    FOREIGN KEY(driver_id)
    REFERENCES Drivers(driver_id)
);

--------------------------------------------------
-- SAMPLE DATA
--------------------------------------------------

INSERT INTO Drivers
(full_name, age, city, signup_date)
VALUES
('John Smith',29,'New York','2025-01-05'),
('Emma Brown',35,'Chicago','2025-01-10'),
('Michael Lee',31,'Los Angeles','2025-01-15'),
('Sarah Wilson',27,'Miami','2025-01-20');

INSERT INTO Verification
(driver_id,documents_submitted,background_check,verified)
VALUES
(1,1,1,1),
(2,1,1,1),
(3,1,0,0),
(4,1,1,1);

INSERT INTO Incentives
(driver_id,incentive_type,incentive_amount)
VALUES
(1,'Signup Bonus',200),
(2,'Referral Bonus',150),
(3,'Signup Bonus',200),
(4,'Weekend Bonus',100);

--------------------------------------------------
-- QUERIES
--------------------------------------------------

-- Activation Rate

SELECT
ROUND(
100 * COUNT(DISTINCT t.driver_id)
/
COUNT(DISTINCT d.driver_id),
2
) AS activation_rate
FROM Drivers d
LEFT JOIN Trips t
ON d.driver_id=t.driver_id;

--------------------------------------------------

-- Active Drivers by City

SELECT
d.city,
COUNT(DISTINCT t.driver_id) active_drivers
FROM Drivers d
JOIN Trips t
ON d.driver_id=t.driver_id
GROUP BY d.city
ORDER BY active_drivers DESC;

--------------------------------------------------

-- Verification Rate

SELECT
ROUND(
100*
SUM(CASE WHEN verified=1 THEN 1 ELSE 0 END)
/COUNT(*),
2
) AS verification_rate
FROM Verification;

--------------------------------------------------

-- Incentive Effectiveness

SELECT
i.incentive_type,
COUNT(DISTINCT t.driver_id) activated_drivers
FROM Incentives i
LEFT JOIN Trips t
ON i.driver_id=t.driver_id
GROUP BY i.incentive_type;

--------------------------------------------------

-- Average Earnings

SELECT
AVG(earnings) avg_earnings
FROM Trips;

--------------------------------------------------

-- Driver Earnings

SELECT
d.full_name,
SUM(t.earnings) total_earnings
FROM Drivers d
JOIN Trips t
ON d.driver_id=t.driver_id
GROUP BY d.full_name
ORDER BY total_earnings DESC;

--------------------------------------------------

-- Monthly Signups

SELECT
YEAR(signup_date) year,
MONTH(signup_date) month,
COUNT(*) signups
FROM Drivers
GROUP BY year,month
ORDER BY year,month;

--------------------------------------------------

-- Trips per Driver

SELECT
d.full_name,
COUNT(t.trip_id) total_trips
FROM Drivers d
LEFT JOIN Trips t
ON d.driver_id=t.driver_id
GROUP BY d.full_name;