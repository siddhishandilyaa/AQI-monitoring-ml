from ckanapi import RemoteCKAN
import pandas as pd

# =========================
# SETTINGS
# =========================
RESOURCE_ID = "f6be929b-151a-4b92-b5b4-507481b15128"
OUTPUT_FILE = "rohini_dpcc_hourly_api.csv"

# =========================
# FETCH DATA FROM API
# =========================
rc = RemoteCKAN("https://data.opencity.in/")

limit = 5000
offset = 0
all_records = []

while True:
    result = rc.action.datastore_search(
        resource_id=RESOURCE_ID,
        limit=limit,
        offset=offset
    )
    records = result["records"]
    if not records:
        break

    all_records.extend(records)
    offset += limit
    print(f"Fetched {len(all_records)} rows...")

# convert to DataFrame
df = pd.DataFrame(all_records)

# =========================
# KEEP ONLY REQUIRED COLUMNS
# =========================
required_cols = [
    "Timestamp",
    "PM2.5 (ug/m3)",
    "PM10 (ug/m3)",
    "NO2 (ug/m3)",
    "CO (mg/m3)"
]

# keep only columns that actually exist
required_cols = [col for col in required_cols if col in df.columns]
df = df[required_cols].copy()

# =========================
# RENAME COLUMNS
# =========================
rename_map = {
    "Timestamp": "Datetime",
    "PM2.5 (ug/m3)": "pm2_5_api",
    "PM10 (ug/m3)": "pm10_api",
    "NO2 (ug/m3)": "no2_api",
    "CO (mg/m3)": "co_api"
}
df = df.rename(columns=rename_map)

# =========================
# CLEAN DATETIME
# =========================
df["Datetime"] = pd.to_datetime(df["Datetime"], errors="coerce")
df = df.dropna(subset=["Datetime"]).sort_values("Datetime").reset_index(drop=True)

# =========================
# CONVERT NUMERIC COLUMNS
# =========================
numeric_cols = ["pm2_5_api", "pm10_api", "no2_api", "co_api"]

for col in numeric_cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

# =========================
# RESAMPLE 15-MIN TO HOURLY
# =========================
df = (
    df.set_index("Datetime")
      .resample("1H")
      .mean(numeric_only=True)
      .reset_index()
)

# =========================
# OPTIONAL DATE + TIME COLUMNS
# =========================
df["Date"] = df["Datetime"].dt.strftime("%d-%m-%Y")
df["time_ist"] = df["Datetime"].dt.strftime("%H:%M:%S")

# =========================
# REORDER COLUMNS
# =========================
final_cols = ["Date", "time_ist", "Datetime", "pm2_5_api", "pm10_api", "no2_api", "co_api"]
final_cols = [col for col in final_cols if col in df.columns]
df = df[final_cols]

# =========================
# SAVE FINAL FILE
# =========================
df.to_csv(OUTPUT_FILE, index=False)

print(f"Saved: {OUTPUT_FILE}")
print(df.head())
print(df.shape)