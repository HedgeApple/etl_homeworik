import pandas as pd
from re import sub
from utility import (
    update_country_alpha3,
    update_ean13,
    create_box_columns,
    update_cost_column,
    column_mapping,
)


def rename_columns(data: pd.DataFrame) -> None:
    """Renames the columns in the dataframe as needed

    Args:
        data (pd.DataFrame): The data to be formatted with the renamed columns
    """
    box_columns = create_box_columns()
    column_mapping.update(box_columns)
    data.rename(columns=column_mapping, inplace=True)


def format_ean13(data: pd.DataFrame) -> pd.DataFrame:
    """Formats the ean13 column. Ex 0000000000000 to 000-000000000-0

    Args:
        data (pd.DataFrame): the data to be formatted

    Returns:
        pd.DataFrame: data updated
    """
    data["ean13"] = data["ean13"].apply(update_ean13)
    return data


def datatype_transformation(data: pd.DataFrame) -> pd.DataFrame:
    data["min_price"] = data["min_price"].apply(update_cost_column)
    data["cost_price"] = data["min_price"].apply(lambda x: f"{(x * 0.69):.2f}")
    data["prop_65"] = True
    data["made_to_order"] = False
    data["manufacturer_sku"] = data["manufacturer_sku"].astype(str)
    data.fillna(value="", axis=1, inplace=True)

    return data


def add_new_columns(data: pd.DataFrame, desired_columns: list) -> pd.DataFrame:
    """Adding empty columns for this specific case

    Args:
        data (pd.DataFrame): the input data to be formatted
        desired_columns (list): the new columns that must be added

    Returns:
        pd.DataFrame: the resulting dataframe with the new columns
    """
    existing_columns = list(data.columns)
    new_columns_to_add = [col for col in desired_columns if col not in existing_columns]
    for col in new_columns_to_add:
        data[col] = ""
    return data


def countries_to_alpha3(data: pd.DataFrame) -> pd.DataFrame:
    """Updates the country names into an alpha3 format

    Args:
        data (pd.DataFrame): the data to be formatted as a dataframe

    Returns:
        pd.DataFrame: the updated dataframe
    """
    data["product__country_of_origin__alpha_3"] = data[
        "product__country_of_origin__alpha_3"
    ].apply(update_country_alpha3)
    return data


def read_csv(filename: str) -> pd.DataFrame:
    """Reads the CSV file from the input data, and reads the output example file to extract the required name columns

    Args:
        filename (str): the path of the input data file

    Returns:
        pd.DataFrame: the data to be formatted
    """
    homework_df = pd.read_csv(filename, header=0, delimiter=",")
    example_df = pd.read_csv("etl_homework/example.csv", header=0, delimiter=",")
    new_columns = list(example_df.columns)
    return homework_df, new_columns


def transform() -> pd.DataFrame:
    """Transformation method. Step by step

    Returns:
        pd.DataFrame: the formatted data
    """
    # Read the CSV file, and separately, the column list from the expected dataframe
    data, new_columns = read_csv("etl_homework/homework.csv")
    # Rename the existing columns to the desired names
    rename_columns(data)
    # Update the countries to be displayed as alpha3
    data = countries_to_alpha3(data)
    data = datatype_transformation(data)
    # Add the desired columns, in this case, are empty
    data = add_new_columns(data, new_columns)
    # Format the ean13 to have the expected '-'
    data = format_ean13(data)
    data = data[new_columns]
    return data, new_columns


if __name__ == "__main__":
    result_df, columns_to_display = transform()
    result_df.to_csv("etl_homework/formatted.csv", columns=columns_to_display)
