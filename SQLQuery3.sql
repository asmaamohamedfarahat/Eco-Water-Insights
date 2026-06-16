-- نقل البيانات هندسياً من الجدول المؤقت إلى جدول الحقائق الرئيسي المدمج
INSERT INTO Fact_Global_Nexus (
    Country_Key, Year_Key, Avg_Global_Temperature, Total_Global_Precipitation,
    Avg_Global_Evaporation, Avg_Global_Soil_Moisture, Production_MT,
    Crops_Tomatoes_Production_Ton, Crops_Wheat_Production_Ton
)
SELECT 
    COUNTRY, YEAR, Avg_Global_Temperature, Total_Global_Precipitation,
    Avg_Global_Evaporation, Avg_Global_Soil_Moisture, Production_MT,
    Crops_Tomatoes_Production_Ton, Crops_Wheat_Production_Ton
FROM Staging_Global_Nexus;
GO