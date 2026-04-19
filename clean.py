import pandas as pd

input_path = "Aqi_data_new.xlsx"
output_path = "Aqi_raw.xlsx"

df = pd.read_excel(input_path)

# Convert blank strings to missing values, then drop fully empty rows
cleaned = df.replace(r'^\s*$', pd.NA, regex=True).dropna(how='all')

# Optionally drop rows with too few valid values
# cleaned = cleaned.dropna(thresh=4)

# Remove columns that are completely empty
cleaned = cleaned.dropna(axis=1, how='all')

cleaned.reset_index(drop=True, inplace=True)

cleaned.to_excel(output_path, index=False)
print(f"Cleaned data saved to {output_path}.")