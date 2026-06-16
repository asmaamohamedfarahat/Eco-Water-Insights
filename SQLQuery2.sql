-- 1. إنشاء قاعدة بيانات مستودع البيانات العالمي والمصري الموحد
CREATE DATABASE Global_And_Egypt_Warehouse_DB;
GO
USE Global_And_Egypt_Warehouse_DB;
GO

-- 2. جدول بُعد الدول (Dim_Country) لتنظيم التصنيفات الجغرافية والقارات
CREATE TABLE Dim_Country (
    Country_Name VARCHAR(150) PRIMARY KEY,
    Continent VARCHAR(50) NOT NULL
);

-- تغذية جدول الدول بالبيانات الجغرافية والقارات للدول الموجودة في الداتا
INSERT INTO Dim_Country VALUES 
('Egypt', 'Africa'), 
('United States', 'North America'), 
('China', 'Asia'), 
('Brazil', 'South America'), 
('Germany', 'Europe'), 
('Australia', 'Australia'),
('India', 'Asia');

-- 3. جدول بُعد الزمن (Dim_Time) لتمكين التحليل التاريخي والمستقبلي
CREATE TABLE Dim_Time (
    Year_ID INT PRIMARY KEY,
    Decade VARCHAR(20)
);

-- ملء جدول السنوات تلقائياً من عام 2000 وحتى 2024
DECLARE @Y INT = 2000;
WHILE @Y <= 2024
BEGIN
    INSERT INTO Dim_Time VALUES (@Y, CAST((@Y / 10) * 10 AS VARCHAR(4)) + 's');
    SET @Y = @Y + 1;
END;
GO

-- 4. جدول الحقائق الرئيسي الشامل (Fact_Global_Nexus) الذي سيستقبل ملف البايثون الموحد
CREATE TABLE Fact_Global_Nexus (
    Fact_ID INT IDENTITY(1,1) PRIMARY KEY,
    Country_Key VARCHAR(150) FOREIGN KEY REFERENCES Dim_Country(Country_Name),
    Year_Key INT FOREIGN KEY REFERENCES Dim_Time(Year_ID),
    Avg_Global_Temperature FLOAT,
    Total_Global_Precipitation FLOAT,
    Avg_Global_Evaporation FLOAT,
    Avg_Global_Soil_Moisture FLOAT,
    Production_MT FLOAT,
    Crops_Tomatoes_Production_Ton FLOAT,
    Crops_Wheat_Production_Ton FLOAT
);
GO