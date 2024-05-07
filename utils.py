from datetime import datetime
from decimal import Decimal


class Utils:

    CONVERTER_CM = 0.393701
    CONVERTER_MM = 0.0393701
    CONVERTER_KG_TO_POUNDS = 2.20462

    @staticmethod
    def process_row(row, header_mapping):
        formatted_row = {}

        for output_field, input_field in header_mapping.items():
            try:
                value = row[input_field]
            except:
                value = ''

            if isinstance(value, str):
                value = value.strip()  # Strip whitespace if it's a string

            if any(field in output_field for field in ['width', 'height', 'depth']) and 'inches' not in output_field:
                value = Utils.convert_to_inches(value, 'inches')
            elif output_field == 'weight':
                value = Utils.convert_to_pounds(value, 'pounds')
            elif output_field == 'upc':
                value = str(value)
            elif output_field == 'system creation date':
                value = Utils.format_date(value)
            elif output_field in ['wholesale ($)', 'map ($)', 'msrp ($)']:
                value = Utils.format_currency(value)
            elif output_field == 'length':
                # Calculate length using furniture dimensions
                length = Utils.calculate_furniture_length(row)
                formatted_row[output_field] = length
                continue
            formatted_row[output_field] = value

        return formatted_row

    @staticmethod
    def convert_to_inches(value, unit):
        try:
            if unit.lower() == 'inches':
                return float(value)
            elif unit.lower() == 'cm':
                return float(value) * Utils.CONVERTER_CM
            elif unit.lower() == 'mm':
                return float(value) * Utils.CONVERTER_MM
            else:
                return float(value)  # Assume already in inches if unknown unit
        except:
            return None

    @staticmethod
    def convert_to_pounds(value, unit):
        if unit.lower() == 'pounds':
            return float(value)
        elif unit.lower() == 'kg':
            return float(value) * Utils.CONVERTER_KG_TO_POUNDS
        else:
            return float(value)

    @staticmethod
    def format_currency(value):
        try:
            return Decimal(value).quantize(Decimal('0.01'))
        except:
            return None

    @staticmethod
    def format_date(date_str):
        try:
            return datetime.strptime(date_str, '%m/%d/%y').strftime('%Y-%m-%d')
        except:
            return None

    @staticmethod
    def calculate_furniture_length(row):
        width = float(row['item width (inches)'])
        depth = float(row['item depth (inches)'])
        height = float(row['item height (inches)'])
        diameter = float(row['item diameter (inches)'])
        dimensions = [width, depth, height, diameter]
        return max(dimensions)

    @staticmethod
    def convert_country_name_to_iso2(country_name):
        ref = {
            "China": "CHN",
            "India": "IND",
            "Indonesia": "IDN",
            "Phillipines": "PHL",
            "Thailand": "THA",
            "Vietnam": "VNM",
        }
        try:
            return ref[country_name]
        except:
            return None

    @staticmethod
    def convert_ul_certified(ul):
        ref = {
            "UL": 'True',
            "UL/CUL": 'True',
        }
        try:
            return ref[ul]
        except:
            return False
