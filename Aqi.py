import pandas as pd
import numpy as np

# ========= 1) LOAD EXCEL FILE =========
input_file = "AQI.xlsx"
df = pd.read_excel(input_file)

# ========= 2) SORT BY DATE TIME =========
df["time"] = pd.to_datetime(df["time"], dayfirst=True, errors="coerce")
df = df.sort_values("time").reset_index(drop=True)

# ========= 3) WRITE YOUR EXACT COLUMN NAMES HERE =========
pm25_col = "pm2_5"   # replace with your exact PM2.5 column name
pm10_col = "pm10"    # replace with your exact PM10 column name
no2_col  = "no2"     # replace with your exact NO2 column name
co_col   = "co"      # replace with your exact CO column name

# ========= 4) INDIAN AQI BREAKPOINTS =========
BREAKPOINTS = {
    "pm2_5": [
        (0, 30, 0, 50),
        (31, 60, 51, 100),
        (61, 90, 101, 200),
        (91, 120, 201, 300),
        (121, 250, 301, 400),
        (251, 1000, 401, 500)
    ],
    "pm10": [
        (0, 50, 0, 50),
        (51, 100, 51, 100),
        (101, 250, 101, 200),
        (251, 350, 201, 300),
        (351, 430, 301, 400),
        (431, 2000, 401, 500)
    ],
    "no2": [
        (0, 40, 0, 50),
        (41, 80, 51, 100),
        (81, 180, 101, 200),
        (181, 280, 201, 300),
        (281, 400, 301, 400),
        (401, 2000, 401, 500)
    ],
    "co": [
        (0, 1.0, 0, 50),
        (1.1, 2.0, 51, 100),
        (2.1, 10.0, 101, 200),
        (10.1, 17.0, 201, 300),
        (17.1, 34.0, 301, 400),
        (34.1, 100.0, 401, 500)
    ]
}

# ========= 5) SUB-INDEX FUNCTION =========
def calc_subindex(conc, pollutant):
    if pd.isna(conc):
        return np.nan

    conc = float(conc)
    ranges = BREAKPOINTS[pollutant]

    for bp_lo, bp_hi, aqi_lo, aqi_hi in ranges:
        if bp_lo <= conc <= bp_hi:
            sub = ((aqi_hi - aqi_lo) / (bp_hi - bp_lo)) * (conc - bp_lo) + aqi_lo
            return round(sub, 2)

    if conc > ranges[-1][1]:
        return 500.0

    return np.nan

# ========= 6) CALCULATE SUB-INDICES =========
df["pm2_5_subindex"] = df[pm25_col].apply(lambda x: calc_subindex(x, "pm2_5"))
df["pm10_subindex"]  = df[pm10_col].apply(lambda x: calc_subindex(x, "pm10"))
df["no2_subindex"]   = df[no2_col].apply(lambda x: calc_subindex(x, "no2"))
df["co_subindex"]    = df[co_col].apply(lambda x: calc_subindex(x, "co"))

# ========= 7) RAW AQI =========
sub_cols = ["pm2_5_subindex", "pm10_subindex", "no2_subindex", "co_subindex"]
df["aqi_raw"] = df[sub_cols].max(axis=1, skipna=True).round(2)

# ========= 8) MAKE AQI LOOK MORE REALISTIC =========
# smooth a little
df["aqi_realistic"] = (
    df["aqi_raw"]
    .rolling(window=3, center=True, min_periods=1)
    .mean()
)

# limit too-sharp jumps
max_change_per_hour = 35

aqi_vals = df["aqi_realistic"].copy()

for i in range(1, len(aqi_vals)):
    prev = aqi_vals.iloc[i - 1]
    curr = aqi_vals.iloc[i]

    if pd.notna(prev) and pd.notna(curr):
        diff = curr - prev
        if diff > max_change_per_hour:
            aqi_vals.iloc[i] = prev + max_change_per_hour
        elif diff < -max_change_per_hour:
            aqi_vals.iloc[i] = prev - max_change_per_hour

df["aqi_realistic"] = aqi_vals.round(2)

# ========= 10) SAVE OUTPUT =========
output_file = "aqi_outputt.xlsx"
df.to_excel(output_file, index=False)

print("Done. Saved as:", output_file)