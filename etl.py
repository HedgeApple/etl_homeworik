import csv
from datetime import datetime
import json
from typing import List, Any, Optional


class ETLService:

    def __init__(self):
        self.columns_mapping = None
        self.input_file_headers = None
        self.output_file_headers = None

    def run(self, input_file: str, output_file: str, columns_mapping_file: str) -> None:
        """Performs the complete ETL process."""

        input_data = self.read_csv(input_file)

        input_data = self.extract_headers(input_data)

        with open(columns_mapping_file, 'r') as f:
            self.columns_mapping = json.load(f)

        transformed_data = self.transform_data(input_data)

        self.output_file_headers = [column for column in self.columns_mapping.values() if column is not None]

        self.write_csv(output_file, transformed_data)

    def extract_headers(self, input_data: List[List[Any]]):
        """Save the headers before removing the first row and remove headers from data."""
        self.input_file_headers = input_data[0] if input_data else []
        if input_data:
            input_data_without_headers = input_data[1:]
            return input_data_without_headers
        else:
            return input_data

    def read_csv(self, filename: str) -> List[List[Any]]:
        """Reads a CSV file and returns the data as a list of rows."""
        data: List[List[Any]] = []
        try:
            with open(filename, 'r', newline='') as file:
                reader = csv.reader(file)
                for row in reader:
                    data.append(row)
        except FileNotFoundError:
            print(f"Error: Could not find the file '{filename}'")
        except Exception as e:
            print(f"Error while reading the file '{filename}': {e}")
        
        return data

    def write_csv(self, filename: str, data: List[List[Any]]) -> None:
        """Writes the data to a CSV file with the provided headers."""
        try:
            with open(filename, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(self.output_file_headers)
                writer.writerows(data)
            print(f"The formatted data has been written to '{filename}'")
        except Exception as e:
            print(f"Error writing to the file '{filename}': {e}")

    def transform_data(
            self, 
            input_data: List[List[Any]], 
        ) -> List[List[Any]]:
        """Transforms the data according to the example headers."""
        transformed_data: List[List[Any]] = []

        for input_row in input_data:
            transformed_row = []
            for column_name in self.input_file_headers:
                
                # Get the input column name corresponding to the output column name
                input_column_index = list(self.columns_mapping.keys()).index(column_name)

                if list(self.columns_mapping.values())[input_column_index] is None:
                    continue

                # Get the value of the input column
                value = input_row[input_column_index]

                transformed_value = self.transform_column_value(column_name, value)
                transformed_row.append(transformed_value)
            transformed_data.append(transformed_row)
        return transformed_data

    def transform_column_value(self, column_name: str, value: Any) -> Any:
        """Transforms the value of a column based on its name."""
        if column_name == 'system creation date':
            return self.date_iso_format_transform(value)
        elif '($)' in column_name:
            return self.round_currency(value)
        elif 'cm' in column_name:
            return self.convert_to_inches(value, 'cm')
        elif 'feet' in column_name:
            return self.convert_to_inches(value, 'feet')
        elif 'kg' in column_name:
            return self.convert_to_pounds(value, 'kg')
        elif 'upc' in column_name or 'gtin' in column_name or 'ean' in column_name:
            return str(value)
        else:
            return value

    def date_iso_format_transform(self, date: str) -> Optional[str]:
        """Transforms a date from the format '7/7/15' to ISO 8601 (YYYY-MM-DD)."""
        try:
            original_date = datetime.strptime(date, '%m/%d/%y')
            iso_date = original_date.strftime('%Y-%m-%d')
            return iso_date
        except ValueError:
            print(f"Error: The date '{date}' does not have the expected format.")
            return date

    def round_currency(self, amount: str) -> str:
        """Rounds the currency amount to the nearest cent."""
        try:
            # Remove the $ sign if present and ensure it has 2 decimal places.
            amount = amount.replace('$', '')
            amount = amount.replace(',', '')

            # Convert the amount to float and round to the nearest cent.
            rounded_amount = round(float(amount), 2)

            # Format the amount as a string with two decimal places.
            formatted_amount = '{:.2f}'.format(rounded_amount)

            return str(formatted_amount)
        except ValueError:
            print(f"Error: The value '{amount}' is not a valid amount.")
            return amount

    def convert_to_inches(self, value: str, unit: str) -> str:
        """
        Converts a given measurement from different length units to inches.
        
        Args:
        - value: The numeric value of the measurement.
        - unit: The unit of measurement (can be 'cm' for centimeters or 'feet' for feet).

        Returns:
        - The value of the measurement converted to inches.
        """
        if value:
            if unit == 'cm':
                # 1 pulgada equivale a 2.54 centímetros
                rounded_amount = round(float(value) / 2.54, 2)
                return str(rounded_amount)
            elif unit == 'feet':
                # 1 feet equal to 12 inches
                rounded_amount = round(float(value) * 12, 2)
                return str(rounded_amount)
        else:
            return value
        
    def convert_to_pounds(self, value: str, unit: str) -> str:
        """
        Converts a given weight measurement from different units to pounds.

        Args:
        - value: The numeric value of the measurement.
        - unit: The unit of measurement (can be 'kg' for kilograms).

        Returns:
        - The value of the measurement converted to pounds.
        """
        if unit == 'kg':
            # 1 kg equal to 2.20462 pounds
            return str(round(float(value) * 2.20462, 2))
