import re
import polars as pl
import pycountry
from logging import Logger

from utilities.units_converter import converter_map


class Normalizer:
    def __init__(self, config: dict, logger: Logger) -> None:
        self.logger = logger
        self.data_config = config["data_config"]
        self.data_columns = config["data_columns"]
        self.data_normalizer = config["data_normalizer"]

    def execute(self, df_base: pl.DataFrame) -> pl.DataFrame:
        """
        Execute all the methods defined in the normalizer.
        """
        pipeline = [
            self.normalize_inches_columns,
            self.normalize_pound_columns,
            self.convert_units_to_float,
            self.convert_currency,
            self.filter_wrong_upcs,
            self.convert_upc_to_ean13,
            self.rename_columns,
            self.normalize_country_column,
            self.format_date_columns,
            self.convert_int_columns,
        ]

        for step in pipeline:
            df_base = step(df_base)

        return df_base

    def convert_units(
        self,
        df_base: pl.DataFrame,
        valid_units: str,
        pattern: re.Pattern,
        replacer: str,
    ) -> pl.DataFrame:
        """
        Function to convert the units.

        Parameters
        ----------
        df_base: pl.DataFrame
            The input DataFrame.
        valid_units: str
            The valid units to convert.
        pattern: re.Pattern
            The regular expression to search for the unit in the column.
        replacer: str
            The replacement string for the new column name.

        Returns
        -------
            pl.DataFrame
        """

        # Get all the columns with valids units.
        if columns_with_units := df_base.select(
            rf"^.*\(({valid_units})\).*$"
        ).columns:
            # For each column, it will convert the values according
            # to the unit matched by the regex.
            for col in columns_with_units:
                result = pattern.findall(col)[0]
                # Replace the old unit with the corresponding one. (inches or pounds)
                new_name = pattern.sub(replacer, col)
                df_base = df_base.with_columns(
                    pl.col(col)
                    .cast(pl.Float64)
                    .map_elements(converter_map[result])
                    .alias(new_name)
                ).drop(col)

        return df_base

    def normalize_inches_columns(self, df_base: pl.DataFrame) -> pl.DataFrame:
        """
        Converts column values that may come in units other than inches.
        It converts from centimeters, meter and feet to inches.
        """
        valid_units = "|".join(self.data_config["inches_units"])
        pattern = re.compile(rf"\(\s*({valid_units})\s*\)")
        return self.convert_units(df_base, valid_units, pattern, "(inches)")

    def normalize_pound_columns(self, df_base: pl.DataFrame) -> pl.DataFrame:
        """
        Converts column values that may come in units other than pound.
        It converts from grams, kilograms and once to pounds.
        """
        valid_units = "|".join(self.data_config["pounds_units"])
        pattern = re.compile(rf"\(\s*({valid_units})\s*\)")
        return self.convert_units(df_base, valid_units, pattern, "(pounds)")

    def convert_units_to_float(self, df_base: pl.DataFrame) -> pl.DataFrame:
        """
        Converts the inches and pound columns to float.
        """
        columns_to_parse = df_base.select(
            r"^.*\(\s*(inches|pounds)\s*\).*$"
        ).columns
        dimension_pattern = re.compile(r".*dimensions?.*")
        for col in columns_to_parse:
            if dimension_pattern.search(col):
                continue
            df_base = df_base.with_columns(pl.col(col).cast(pl.Float64))

        return df_base

    def convert_currency(self, df_base: pl.DataFrame) -> pl.DataFrame:
        """
        Get all the currency columns, replace the unwanted characters
        and format with 2 decimal places.
        """

        # Regex pattern to get all the columns that has the $ symbol.
        column_name_pattern = r"^[^$]*\(\$\)[^$]*$"
        currency_columns = df_base.select(column_name_pattern).columns
        values_pattern = r"[^\d.]"

        return df_base.with_columns(
            [
                pl.col(col)
                .fill_null("0.00")
                .str.replace_all(values_pattern, "")
                .cast(pl.Float64)
                .map_elements(lambda x: f"{x:.2f}", return_dtype=pl.String)
                for col in currency_columns
            ]
        )

    def filter_wrong_upcs(self, df_base: pl.DataFrame) -> pl.DataFrame:
        """
        It filters out the upcs that are null and saves the resulting dataframe.
        We can then report these missing upcs to the corresponding client.
        """
        mask_wrong_upc = pl.col("upc").is_null()

        wrong_upc_quantity = df_base.filter(mask_wrong_upc).shape[1]
        self.logger.warning(
            f"[NORMALIZER] Removed {wrong_upc_quantity} null upcs."
        )

        return df_base.filter(~mask_wrong_upc)

    def convert_upc_to_ean13(self, df_base: pl.DataFrame) -> pl.DataFrame:
        """
        It converts the upc column to ean13 column.
        """
        self.logger.info("[NORMALIZER] Converting upc to ean13.")
        return df_base.with_columns(
            pl.format(
                "0{}-{}-{}",
                pl.col("upc").str.slice(0, length=2),
                pl.col("upc").str.slice(2, length=9),
                pl.col("upc").str.slice(-1),
            ).alias("upc")
        )

    def rename_columns(self, df_base: pl.DataFrame) -> pl.DataFrame:
        """
        Rename the columns according to the names defined in the configuration file.
        """
        self.logger.info("[NORMALIZER] Renaming columns.")
        return df_base.rename(self.data_normalizer)

    def normalize_country_column(self, df_base: pl.DataFrame) -> pl.DataFrame:
        """
        Normalizes the columns with the alpha_3 standard,
        the library pycountry was used to get them
        """

        self.logger.info(
            "[NORMALIZER] Converting all countries to the alpha_3 standard."
        )
        valid_countries = (
            df_base.filter(
                pl.col("product__country_of_origin__alpha_3").is_not_null()
            )["product__country_of_origin__alpha_3"]
            .unique()
            .to_list()
        )
        country_codes = {
            country.name: country.alpha_3
            for country in pycountry.countries
            if country.name in valid_countries
        }

        return df_base.with_columns(
            pl.col("product__country_of_origin__alpha_3").map_dict(
                country_codes
            )
        )

    def format_date_columns(self, df_base: pl.DataFrame) -> pl.DataFrame:
        """
        Converts string columns to date according to the format
        defined in the config file.
        """

        self.logger.info(
            "[NORMALIZER] Converting all date columns to ISO 8601."
        )
        return df_base.with_columns(
            pl.col(self.data_columns["date_columns"]).str.strptime(
                pl.Datetime, self.data_config["date_format"]
            )
        )

    def convert_int_columns(self, df_base: pl.DataFrame) -> pl.DataFrame:
        """
        Convert the string columns defined in the config file into integer columns.
        It'll only convert the columns that are in the list: int_columns
        """
        return df_base.with_columns(
            pl.col(self.data_columns["int_columns"]).cast(pl.Int64).fill_null(0)
        )
