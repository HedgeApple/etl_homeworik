from pycountry_convert import country_name_to_country_alpha3
from re import sub
from decimal import Decimal
from typing import Any

column_mapping = {
    # homework : example
    "description": "product__title",
    "brand": "product__brand__name",
    "item category": "product__product_class__name",
    "country of origin": "product__country_of_origin__alpha_3",
    "item materials": "attrib__material",
    "item finish": "attrib__finish",
    "item style": "product__styles",
    "item number": "manufacturer_sku",
    "item width (inches)": "width",
    "item height (inches)": "height",
    "item weight (pounds)": "weight",
    "item length (inches)": "length",
    "upc": "ean13",  # Must be formatted
    "map ($)": "min_price",
    "msrp ($)": "cost_price",
}


def create_box_columns() -> dict:
    """This method creates specific columns attached to an index.

    Returns:
        dict: a dictionary with all the 'indexed' columns
    """
    new_indexed_columns = {}
    for i in range(0, 3):
        new_indexed_columns[f"carton {i+1} width (inches)"] = f"boxes__{i}__width"
        new_indexed_columns[f"carton {i+1} length (inches)"] = f"boxes__{i}__length"
        new_indexed_columns[f"carton {i+1} height (inches)"] = f"boxes__{i}__height"
        new_indexed_columns[f"carton {i+1} weight (pounds)"] = f"boxes__{i}__weight"

    return new_indexed_columns


def update_country_alpha3(x: str) -> str:
    """Updates the country to alpha3 convention using a specific library

    Args:
        x (str): the country to be updated

    Returns:
        str: the country in alpha3 format or "" if it encounters an issue
    """
    try:
        return country_name_to_country_alpha3(x)
    except:
        return ""


def update_ean13(x: str) -> str:
    """Updates the string from ean13 to the desired output

    Args:
        x (str): the original string

    Returns:
        str: the string formatted into the desired format
    """
    try:
        x = str(int(x))
        return f"0{x[0:2]}-{x[2:len(x)-1]}-{x[-1]}"
    except:
        return ""


def update_cost_column(x: Any) -> Any:
    """Updates the cost column. Depending on the datatype, it must return a float

    Args:
        x (Any): the cost value to be updated

    Returns:
        Any: depending on the case, the cost or zero (0) is returned (when no value is found)
    """
    try:
        if isinstance(x, str):
            # return Decimal(sub(r"[^\d.]", "", x))
            return float(sub("^\$", "", x))
        if isinstance(x, float):
            return x
    except:
        return 0
