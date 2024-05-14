"""
Submodule containing Converter class for translating certain strings.
"""

# Python Built-In Imports
from decimal import Decimal, ROUND_HALF_UP
from re import match

# Custom Imports
from config import ALPHA_3, DistanceMetric, RegexStrings, WeightMetric

# Dictionary for converting words that are numbers to their digit strings.
WORD_NUMS = {
    'one': '1',
    'two': '2',
    'three': '3',
    'four': '4',
    'five': '5',
    'six': '6',
    'seven': '7',
    'eight': '8',
    'nine': '9',
    'ten': '10'
    }

class Converter:
    """
    Class containing static methods for converting specific strings.
        - format_currency(): Forces real number to two decimal places.
        - get_alpha_3(): Returns corresponding alpha 3 code for given country name.
        - set_word_to_num(): Changes words that are numbers to their digit form in strings that indicate product set sizes.
        - to_inches(): Converts a value from the given distance metric to inches.
        - to_pounds(): Converts a value from the given weight metric to pounds.
        - YN_to_bool(): Converts a value from 'Yes' or 'No' to True and False respectively.
    """
    @staticmethod
    def format_currency(value: str) -> str:
        """
        Forces any non-empty string currency to two decimal places.
        Errors on any non-empty string that doesn't match expected currency format.
        
        Args:
            - value: The string value to be converted / rounded.
        
        Returns:
            - The value converted / rounded to two decimal places.
        """
        value = value.replace('$', '').replace(',', '') # Only non-digit character we want to preserve is '.'
        if value == "":
            return value
        elif match(RegexStrings.REAL_POS, value):
            return str(Decimal(value).quantize(Decimal('.01'), rounding=ROUND_HALF_UP))
        else:
            raise RuntimeError(f"Invalid currency value: {value}")

    @staticmethod
    def get_alpha_3(country: str) -> str:
        """
        Function that retrieves a country alpha 3 code while
        checking for some common / expected typos or erros.

        Args:
            - country: The string containing the country's name.

        Returns:
            - A string of the country's corresponding Alpha 3 code.
        """
        if country in ALPHA_3.keys():
            return ALPHA_3[country]
        else:
            match country: # Handle known errors / typos.
                case "":
                    return ""
                case "Phillipines":
                    return "PH"
                case "Vietnam":
                    return "VN"
                case _: # Error out on unknown errors / typos.
                    raise RuntimeError(f"Encountered new error / typo in country: {country}")
    
    @staticmethod
    def set_word_to_num(value: str) -> str:
        """
        Converts a word to a number when used to denote the
        number of products in a set in the given value.

        Args:
            - value: The string value to be converted.

        Returns:
            - A string of the value where every word denoting the
              size of a set is converted to its digit form.
        """
        value = value.lower()
        for key in WORD_NUMS:
            if key in value:
                value = value.replace(f'set of {key}', f'set of {WORD_NUMS[key]}')
        return value

    @staticmethod
    def to_inches(value: str, metric: DistanceMetric) -> str:
        """
        Convert a value in a dimension metric to its equivalent in inches (inch).
        
        Args:
            - value: The string value to be converted.
            - metric: The initial metric to convert from.

        Returns:
            - The value converted to pounds.
        """
        if value == "" or metric == DistanceMetric.inch:
            return value
        elif match(RegexStrings.REAL_POS, value):
            value = float(value)
            match metric:
                case DistanceMetric.cm:
                    return str(value * 0.3937)
                case DistanceMetric.m:
                    return str(value * 39.37)
                case DistanceMetric.ft:
                    return str(value * 12)
                case DistanceMetric.yd:
                    return str(value * 36)
        else:
            raise RuntimeError(f"Invalid distance value: {value}")

    @staticmethod
    def to_pounds(value: str, metric: WeightMetric) -> str:
        """
        Convert a value in a dimension metric to its equivalent in pounds (lb).
        
        Args:
            - value:The string value to be converted.
            - metric: The initial metric to convert from.

        Returns:
            - The value converted to inches.
        """
        if value == "" or metric == WeightMetric.lb:
            return value
        elif match(RegexStrings.REAL_POS, value):
            value = float(value)
            match metric:
                case WeightMetric.t:
                    return str(value * 2204.623)
                case WeightMetric.kg:
                    return str(value * 2.204623)
                case WeightMetric.g:
                    return str(value * 0.002204623)
                case WeightMetric.oz:
                    return str(value * 0.0625)
        else:
            raise RuntimeError(f"Invalid weight value: {value}")
        
    @staticmethod
    def YN_to_bool(value: str) -> str:
        """
        Convert a value from the strings 'Yes' or 'No' to
        their boolean equivalents, True or False, respectively.
        """
        if value == "":
            return value
        elif "yes" in value.lower():
            return True
        elif "no" in value.lower():
            return False
        else:
            raise RuntimeError(f"Invalid value for conversion to boolean: {value}")