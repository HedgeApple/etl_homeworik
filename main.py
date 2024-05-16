from utils import DataTransformer

def ean13_converter(value:str):
    """
    Converts a string to a formatted EAN-13 string.

    Args:
        value (str): The string to convert.

    Returns:
        str: The formatted 13-character EAN-13 code.

    Notes:
         - If the input is not a 12-character string, this method will silently ignore any extra characters.
    """
    value=str(value)
    final_text = value
    if len(value) == 12:
        final_text = '0{}-{}-{}'.format(value[:2],value[2:11],value[11:])
    
    return final_text

def price_converter(value:str):
    """
    Converts a price string to a decimal value with two decimal places.

    Args:
        value (str): The price string to convert.

    Returns:
        float: The converted price value rounded to two decimal places.

    Notes:
         - This method assumes the input string is in the format of "$X,XXX.XX" and removes any non-numeric characters.
    """
    value = str(value).replace('$','').replace(',','')
    return round(float(value),2)

def bool_true_converter(value:str):
    """
    Returns always True no matter the input.

    Args:
        value (str): The input string to convert. It will be ignored

    Returns:
        bool: Always returns True.

    Notes:
         - This method is a simple way to return True on each apply inside `DataTransformer.apply_transformations`.
    """
    return True

def bool_false_converter(value:str):
    """
    Returns always False no matter the input.

    Args:
        value (str): The input string to convert. It will be ignored

    Returns:
        bool: Always returns False.

    Notes:
         - This method is a simple way to return False on each apply inside `DataTransformer.apply_transformations`.
    """
    return False

if __name__ == '__main__':
    etl_transformer = DataTransformer()
    etl_transformer.register_transformation('ean13',ean13_converter)
    etl_transformer.register_transformation('cost_price',price_converter)
    etl_transformer.register_transformation('min_price',price_converter)
    etl_transformer.register_transformation('prop_65',bool_true_converter)
    etl_transformer.register_transformation('made_to_order',bool_false_converter)
    etl_transformer.filter_columns()
    etl_transformer.apply_transformations()
    etl_transformer.dump_frame(filename='formatted.csv')