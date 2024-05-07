import pandas as pd
import json
from utils import Utils

# Load header mapping from JSON file
with open('mapping.json', 'r') as json_file:
    header_mapping = json.load(json_file)

# Define input and output filenames
input_file = 'homework.csv'
output_file = 'formatted.csv'

# Read input CSV file using pandas
df = pd.read_csv(input_file)

# Process each row using the header mapping and Utils
formatted_rows = []
for index, row in df.iterrows():
    formatted_row = Utils.process_row(row, header_mapping)

    # If using separate columns for width and depth
    width = formatted_row.get('furniture seat width (inches)', None)
    depth = formatted_row.get('furniture seat depth (inches)', None)

    formatted_row['attrib__seat_width'] = width
    formatted_row['attrib__seat_depth'] = depth

    formatted_rows.append(formatted_row)

# Create a DataFrame from the list of formatted rows
formatted_df = pd.DataFrame(formatted_rows)

# Drop columns starting with '_'
columns_to_drop = [col for col in formatted_df.columns if col.startswith('_')]
df_filtered = formatted_df.drop(columns=columns_to_drop)

df_filtered['product__country_of_origin__alpha_3'] = df_filtered['product__country_of_origin__alpha_3'].apply(Utils.convert_country_name_to_iso2)
df_filtered['attrib__ul_certified'] = df_filtered['attrib__ul_certified'].apply(Utils.convert_ul_certified)
df_filtered['ean13'] = df_filtered['ean13'].astype(str)

df_filtered.to_csv(output_file, index=False)

print(f"Transformation completed. Transformed data written to '{output_file}'.")
