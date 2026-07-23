
SELECT
Attrition,
COUNT(*) Employees
FROM HR_Employees
GROUP BY Attrition;

SELECT
Department,
Attrition,
COUNT(*) Employees
FROM HR_Employees
GROUP BY Department, Attrition
ORDER BY Department;

SELECT
JobRole,
COUNT(*) Attritions
FROM HR_Employees
WHERE Attrition='Yes'
GROUP BY JobRole
ORDER BY Attritions DESC;

SELECT
OverTime,
Attrition,
COUNT(*) Total
FROM HR_Employees
GROUP BY OverTime, Attrition;

SELECT
Attrition,
AVG(MonthlyIncome) AvgIncome
FROM HR_Employees
GROUP BY Attrition;

SELECT
Attrition,
AVG(DistanceFromHome) AvgDistance
FROM HR_Employees
GROUP BY Attrition;

SELECT
JobSatisfaction,
COUNT(*) TotalEmployees
FROM HR_Employees
GROUP BY JobSatisfaction
ORDER BY JobSatisfaction;

SELECT
JobRole,
AVG(MonthlyIncome) AvgIncome,
AVG(JobSatisfaction) AvgSatisfaction,
AVG(WorkLifeBalance) AvgBalance

FROM HR_Employees

WHERE Attrition='Yes'

GROUP BY JobRole;

