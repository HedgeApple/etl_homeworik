#HedgeApple Challenge by Nicolas

import pandas as pd

# Read and preprocess the data
def read_preprocess_data(file_path):
    # Read the data
    data = pd.read_csv(file_path, low_memory = False)
    
    # Convert column names to lowercase
    data.columns = data.columns.str.lower()
    
    # Index on the 'item number' column
    data.set_index('item number', inplace = True)
    
    return data
 
# Change dates to ISO 8601 format
def format_dates(data):
    date_columns = data.filter(like = 'date').columns
    for column in date_columns:
        data[column] = pd.to_datetime(data[column], format = '%m/%d/%y').dt.strftime('%Y-%m-%d')
    return data

# Format currency
def format_currency(data):
    currency_columns = data.filter(like = '($)').columns
    for column in currency_columns:
        data[column] = data[column].replace('[$,]', '', regex = True).astype(float).round(2).map('${:,.2f}'.format)
    return data

# Convert measurements to inches
def convert_to_inches(data):
    conversion_factors_length = {'inches': 1, 'feet': 12, 'centimeters': 0.393701}
    for key, val in conversion_factors_length.items():
        columns = data.filter(like = key).columns
        for column in columns:
            data[column] *= val
    return data

# Convert weights to pounds
def convert_to_pounds(data):
    conversion_factors_weight = {'pounds': 1, 'kilograms': 2.20462}
    for key, val in conversion_factors_weight.items():
        columns = data.filter(like = key).columns
        for column in columns:
            data[column] *= val
    return data

# Handle UPC / Gtin / EAN as Strings
def convert_to_strings(data):
    columns_to_convert = ['upc', 'gtin', 'ean']
    for column in columns_to_convert:
        if column in data.columns:
            data[column] = data[column].astype(str)
    return data

# Preserve floating point numbers
def preserve_floats(data):
    # There is no operation needed, as Pandas by default preserves floating point numbers
    return data

# Write data to CSV
def write_to_csv(data, file_path):
    data.to_csv(file_path)

# Main function
def main():
    file_path = "homework.csv"
    
    # Read and preprocess the data
    data = read_preprocess_data(file_path)
    
    # Apply transformations
    data = format_dates(data)
    data = format_currency(data)
    data = convert_to_inches(data)
    data = convert_to_pounds(data)
    data = convert_to_strings(data)
    data = preserve_floats(data)
    
    # Write to CSV
    write_to_csv(data, "formatted.csv")

if __name__ == "__main__":
    main()
