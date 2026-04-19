import pandas as pd
from datetime import timedelta

input_path = "Aqi_raw.xlsx"
output_path = "Aqi_1hr data.xlsx"

# set the first date
start_date = pd.Timestamp("2026-01-04")

df = pd.read_excel(input_path)

# Replace this with your actual time column name from the file
# Your file uses `time_ist`.
time_col = "time_ist"
date_col = "Date"

if time_col not in df.columns:
    raise KeyError(f"Missing expected time column: {time_col}. Available columns: {list(df.columns)}")

# Parse the time values
df[time_col] = pd.to_datetime(df[time_col], errors="coerce").dt.time

current_date = start_date
prev_time = pd.Timestamp("00:00").time()
dates = []

for t in df[time_col]:
    if pd.isna(t):
        dates.append(pd.NaT)
        continue

    # when time goes backward, assume next day begins
    if t < prev_time:
        current_date += timedelta(days=1)

    dates.append(current_date)
    prev_time = t

df["Date"] = dates

df.to_excel(output_path, index=False)
print(f"Saved with dates to {output_path}")