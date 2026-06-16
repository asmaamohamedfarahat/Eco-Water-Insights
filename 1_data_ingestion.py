import os
import pandas as pd
import numpy as np

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_DATA_DIR = os.path.join(BASE_DIR, "data", "raw")
os.makedirs(RAW_DATA_DIR, exist_ok=True)

print("==========================================================")
print("-> جاري تشغيل محاكي البيانات الضخمة [EcoWater Insights]")
print("-> توليد بيانات الطقس والمياه لـ 27 محافظة مصرية...")
print("==========================================================")

egypt_provinces = {
    "Cairo": {"lat": 30.04, "zone": "Delta"}, "Giza": {"lat": 30.01, "zone": "Delta"},
    "Alexandria": {"lat": 31.20, "zone": "Coastal"}, "Qalyubia": {"lat": 30.41, "zone": "Delta"},
    "Gharbia": {"lat": 30.78, "zone": "Delta"}, "Monufia": {"lat": 30.59, "zone": "Delta"},
    "Dakahlia": {"lat": 31.03, "zone": "Delta"}, "Kafr El-Sheikh": {"lat": 31.11, "zone": "Coastal"},
    "Sharqia": {"lat": 30.60, "zone": "Delta"}, "Beheira": {"lat": 30.92, "zone": "Delta"},
    "Damietta": {"lat": 31.41, "zone": "Coastal"}, "Port Said": {"lat": 31.25, "zone": "Coastal"},
    "Ismailia": {"lat": 30.60, "zone": "Delta"}, "Suez": {"lat": 29.96, "zone": "Delta"},
    "Fayoum": {"lat": 29.30, "zone": "Upper_Egypt_North"}, "Beni Suef": {"lat": 29.07, "zone": "Upper_Egypt_North"},
    "Minya": {"lat": 28.08, "zone": "Upper_Egypt_North"}, "Asyut": {"lat": 27.17, "zone": "Upper_Egypt_South"},
    "Sohag": {"lat": 26.55, "zone": "Upper_Egypt_South"}, "Qena": {"lat": 26.15, "zone": "Upper_Egypt_South"},
    "Luxor": {"lat": 25.68, "zone": "Upper_Egypt_South"}, "Aswan": {"lat": 24.08, "zone": "Upper_Egypt_South"},
    "Matrouh": {"lat": 31.35, "zone": "Coastal"}, "New Valley": {"lat": 25.43, "zone": "Desert"},
    "Red Sea": {"lat": 26.72, "zone": "Desert"}, "North Sinai": {"lat": 31.12, "zone": "Coastal"},
    "South Sinai": {"lat": 28.53, "zone": "Desert"}
}

years = list(range(2000, 2024))
months = list(range(1, 13))
all_records = []
np.random.seed(100)

for gov_name, info in egypt_provinces.items():
    for year in years:
        for month in months:
            zone = info["zone"]
            if zone == "Upper_Egypt_South":
                base_temp = 26.0 if month in [3,4,10,11] else (38.0 if month in [5,6,7,8,9] else 16.0)
            elif zone == "Upper_Egypt_North" or zone == "Desert":
                base_temp = 23.0 if month in [3,4,10,11] else (34.0 if month in [5,6,7,8,9] else 14.0)
            else:
                base_temp = 20.0 if month in [3,4,10,11] else (30.0 if month in [5,6,7,8,9] else 13.0)
                
            climate_change = (year - 2000) * 0.05
            t2m = round(base_temp + np.random.uniform(-2.0, 2.0) + climate_change, 2)
            prectotcorr = round(np.random.uniform(8.0, 30.0), 2) if zone == "Coastal" and month in [11,12,1,2] else round(np.random.uniform(0.0, 1.0), 2)
            evap = round((t2m * 0.18) + np.random.uniform(1.0, 2.5), 2) if zone in ["Upper_Egypt_South", "Desert"] else round((t2m * 0.13) + np.random.uniform(0.5, 1.5), 2)
            gwetprof = round(0.4 - (evap * 0.04) + np.random.uniform(-0.03, 0.03), 2) if zone in ["Desert", "Upper_Egypt_South"] else round(0.75 - (evap * 0.05) + np.random.uniform(-0.04, 0.04), 2)
            
            all_records.append({
                "YEAR": year, "MO": month, "Governorate": gov_name,
                "T2M": t2m, "PRECTOTCORR": prectotcorr, "EVAP": evap, "GWETPROF": max(0.05, min(0.95, gwetprof))
            })

df = pd.DataFrame(all_records)
output_path = os.path.join(RAW_DATA_DIR, "egypt_climate_water_raw.csv")
df.to_csv(output_path, index=False)

print(f"[نجاح] تم توليد {len(df)} سطر وحفظ الملف في: {output_path}")