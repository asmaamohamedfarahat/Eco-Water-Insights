from pyspark.sql import SparkSession
from pyspark.sql import functions as F

# تهيئة بيئة Spark
spark = SparkSession.builder \
    .appName("EcoWater_Nexus_Processing") \
    .getOrCreate()

# المسارات
global_crops_path = "global_data/clean/real_global_crops.csv"
global_env_fish_path = "global_data/clean/real_global_env_fish.csv"
egypt_file_path = "egypt_data/egypt_nexus_data.csv"
output_dir = "global_data/final_processed/final_combined_nexus_data"

# قراءة البيانات
global_crops_df = spark.read.csv(global_crops_path, header=True, inferSchema=True)
global_env_df = spark.read.csv(global_env_fish_path, header=True, inferSchema=True)

# الـ Pivot
global_crops_pivoted = global_crops_df.groupBy("COUNTRY", "YEAR") \
    .pivot("CROP_ITEM") \
    .sum("PRODUCTION_TONS") \
    .withColumnRenamed("Wheat", "Crops_Wheat_Production_Ton") \
    .withColumnRenamed("Tomatoes", "Crops_Tomatoes_Production_Ton")

# الـ Join
final_global_df = global_env_df.join(global_crops_pivoted, on=["COUNTRY", "YEAR"], how="inner")

# دمج داتا مصر (Union)
egypt_df = spark.read.csv(egypt_file_path, header=True, inferSchema=True) \
    .withColumn("COUNTRY", F.lit("Egypt")) \
    .withColumnRenamed("Avg_Egypt_Temperature", "Avg_Global_Temperature") \
    .withColumnRenamed("Total_Egypt_Precipitation", "Total_Global_Precipitation") \
    .withColumnRenamed("Avg_Egypt_Evaporation", "Avg_Global_Evaporation") \
    .withColumnRenamed("Avg_Egypt_Soil_Moisture", "Avg_Global_Soil_Moisture")

# التوحيد النهائي
complete_nexus_matrix = final_global_df.unionByName(egypt_df)

# التصدير
complete_nexus_matrix.write.mode("overwrite").csv(output_dir, header=True)
spark.stop()