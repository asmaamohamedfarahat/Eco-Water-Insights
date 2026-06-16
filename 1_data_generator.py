import os
import pandas as pd
import numpy as np

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_DATA_DIR = os.path.join(BASE_DIR, "data", "raw")
os.makedirs(RAW_DATA_DIR, exist_ok=True)

print("==========================================================")
print("-> Starting EcoWater synthetic data generator...")
print("-> Generating climate and water metrics for Egypt governorates...")
print("==========================================================")

egypt_provinces = {
    "Cairo": {"zone": "Delta"},
    "Giza": {"zone": "Delta"},
    "Alexandria": {"zone": "Coastal"},
    "Qalyubia": {"zone": "Delta"},
    "Gharbia": {"zone": "Delta"},
    "Monufia": {"zone": "Delta"},
    "Dakahlia": {"zone": "Delta"},
    "Kafr El-Sheikh": {"zone": "Coastal"},
    "Sharqia": {"zone": "Delta"},
    "Beheira": {"zone": "Delta"},
    "Damietta": {"zone": "Coastal"},
    "Port Said": {"zone": "Coastal"},
    "Ismailia": {"zone": "Delta"},
    "Suez": {"zone": "Delta"},
    "Fayoum": {"zone": "Upper_Egypt_North"},
    "Beni Suef": {"zone": "Upper_Egypt_North"},
    "Minya": {"zone": "Upper_Egypt_North"},
    "Asyut": {"zone": "Upper_Egypt_South"},
    "Sohag": {"zone": "Upper_Egypt_South"},
    "Qena": {"zone": "Upper_Egypt_South"},
    "Luxor": {"zone": "Upper_Egypt_South"},
    "Aswan": {"zone": "Upper_Egypt_South"},
    "Matrouh": {"zone": "Coastal"},
    "New Valley": {"zone": "Desert"},
    "Red Sea": {"zone": "Desert"},
    "North Sinai": {"zone": "Coastal"},
    "South Sinai": {"zone": "Desert"}
}

years = list(range(2015, 2025))
months = list(range(1, 13))
all_records = []

np.random.seed(123)

for gov, info in egypt_provinces.items():
    for year in years:
        for month in months:
            zone = info["zone"]
            if zone == "Upper_Egypt_South":
                base_temp = 26.0 if month in [3, 4, 10, 11] else (38.0 if month in [5, 6, 7, 8, 9] else 16.0)
            elif zone in ["Upper_Egypt_North", "Desert"]:
                base_temp = 23.0 if month in [3, 4, 10, 11] else (34.0 if month in [5, 6, 7, 8, 9] else 14.0)
            else:
                base_temp = 20.0 if month in [3, 4, 10, 11] else (30.0 if month in [5, 6, 7, 8, 9] else 13.0)

            climate_trend = (year - 2015) * 0.04
            t2m = round(base_temp + np.random.uniform(-2.0, 2.0) + climate_trend, 2)
            prectotcorr = round(np.random.uniform(0.0, 40.0) if zone == "Coastal" and month in [11, 12, 1, 2] else np.random.uniform(0.0, 5.0), 2)
            evap = round((t2m * (0.16 if zone in ["Upper_Egypt_South", "Desert"] else 0.12)) + np.random.uniform(0.7, 2.0), 2)
            gwetprof = round(0.4 - (evap * 0.04) + np.random.uniform(-0.03, 0.03), 2) if zone in ["Desert", "Upper_Egypt_South"] else round(0.75 - (evap * 0.05) + np.random.uniform(-0.04, 0.04), 2)

            all_records.append({
                "YEAR": year,
                "MONTH": month,
                "Governorate": gov,
                "Zone": zone,
                "T2M": t2m,
                "PRECTOTCORR": max(0.0, prectotcorr),
                "EVAP": evap,
                "GWETPROF": max(0.05, min(0.95, gwetprof))
            })

output_file = os.path.join(RAW_DATA_DIR, "egypt_climate_water_generated.csv")
df = pd.DataFrame(all_records)
df.to_csv(output_file, index=False)

print(f"[SUCCESS] Generated {len(df)} records and saved to: {output_file}")
