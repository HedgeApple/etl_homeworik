import polars as pl
import re
from logging import Logger


class Transform:
    def __init__(self, config: dict, logger: Logger):
        self.logger = logger
        self.data_columns = config["data_columns"]
        self.data_config = config["data_config"]

        self.boxes_columns = []
        self.bullets_columns = []
        self.dimensions_columns = []

    def execute(self, df_base: pl.DataFrame) -> pl.DataFrame:
        """
        Execute all the methods defined in the transform.
        """
        pipeline = [
            self.create_prop65_column,
            self.create_design_id_column,
            self.create_ul_certified_column,
            self.create_product_styles_column,
            self.create_parent_sku_column,
            self.create_made_to_order_column,
            self.calculate_bulbs,
            self.create_boxes_columns,
            self.create_bullets_columns,
            self.transform_dimensions,
            self.transform_boolean_columns,
            self.handle_missing_weight,
            # self.create_unknow_columns,
            self.reorder_columns,
        ]

        for step in pipeline:
            df_base = step(df_base)

        return df_base

    def create_prop65_column(self, df_base: pl.DataFrame) -> pl.DataFrame:
        """
        Creates the column 'prop65', which is related to Proposition 65,
        which points out products that can expose the user to chemical agents.
        """
        return df_base.with_columns(
            pl.when(pl.col("prop__65").is_not_null())
            .then(pl.lit(True))
            .otherwise(pl.lit(False))
            .alias("prop__65")
        )

    @staticmethod
    def create_design_id_column(df_base: pl.DataFrame) -> pl.DataFrame:
        """
        Creates the 'design_id' column.
        It takes the first 10 digits of the designer name hash.
        """
        return df_base.with_columns(
            pl.when(pl.col("attrib__designer").is_not_null())
            .then(
                pl.col("attrib__designer")
                .hash()
                .cast(pl.String)
                .str.slice(0, 10)
            )
            .otherwise(pl.lit(None))
            .alias("attrib__design_id")
        )

    @staticmethod
    def create_ul_certified_column(df_base: pl.DataFrame) -> pl.DataFrame:
        """
        Creates the 'ul_certified' column.
        """
        return df_base.with_columns(
            pl.when(
                pl.col("attrib__ul_certified")
                .str.to_lowercase()
                .str.contains("ul")
            )
            .then(pl.lit(True))
            .otherwise(pl.lit(False))
            .alias("attrib__ul_certified")
        )

    @staticmethod
    def create_product_styles_column(df_base: pl.DataFrame) -> pl.DataFrame:
        """
        Creates the 'product_styles' column.
        It splits the 'item substyle' column by the / character
        then takes the first item of this split and
        concatenates it with the column 'item substyle 2'
        """
        return df_base.with_columns(
            (
                pl.format(
                    "{} {}",
                    pl.col("item substyle")
                    .str.split("/")
                    .list.get(0)
                    .str.strip(),
                    pl.col("item substyle 2"),
                )
            ).alias("product__styles")
        )

    @staticmethod
    def create_parent_sku_column(df_base: pl.DataFrame) -> pl.DataFrame:
        """
        Creates the 'product__parent_sku' column
        to group together product variants of the same brand.
        """

        # It groups the "manufacturer_sku" column by the "product__brand__name"
        # and "product__product_class__name" columns.
        df_groupby = df_base.group_by(
            ["product__brand__name", "product__product_class__name"]
        ).agg(pl.col("manufacturer_sku").unique())
        # Then gets the first letter of the "product__brand__name" column
        # and the first 3 digits of the hash of that column,
        # then concatenates the first 4 digits of the
        # "product__product_class__name" column hash
        # Example: "Dimond Home" and "Indoor Lighting"
        # it'll be "D-3042152"
        df_parent_skus = df_groupby.with_columns(
            pl.format(
                "{}-{}{}",
                pl.col("product__brand__name").str.slice(0, 1),
                pl.col("product__brand__name")
                .hash()
                .cast(pl.String)
                .str.slice(0, 3),
                pl.col("product__product_class__name")
                .hash()
                .cast(pl.String)
                .str.slice(0, 4),
            ).alias("product__parent_sku"),
        )

        # Join the two dataframes by the columns
        # "product__brand__name" and "product__product_class__name"
        # to get the "product__parent_sku"
        return df_base.join(
            df_parent_skus,
            on=["product__brand__name", "product__product_class__name"],
            how="left",
        )

    def create_made_to_order_column(
        self, df_base: pl.DataFrame
    ) -> pl.DataFrame:
        return df_base.with_columns(pl.lit(False).alias("made_to_order"))

    @staticmethod
    def calculate_bulbs(df_base: pl.DataFrame) -> pl.DataFrame:
        """
        Creates the 'attrib__number_bulbs' with the sum of values in both columns 'bulb 1
        count' and 'bulb 2 count'
        """
        return df_base.with_columns(
            (pl.col("bulb 1 count") + pl.col("bulb 2 count")).alias(
                "attrib__number_bulbs"
            ),
        )

    def create_boxes_columns(self, df_base: pl.DataFrame) -> pl.DataFrame:
        """
        Creates the 'boxes' columns
        """

        # Regex to get all the "carton" columns
        # since 'select' doesnt accept Pattern it will compile it after.
        regex_str = r"^carton\s*(\d+)\s*(.*)$"
        columns = df_base.select(regex_str).columns
        pattern = re.compile(regex_str)
        # Valid units for these columns

        dimension_pattern = re.compile(r"\s*\(\w*\)")
        # Creates a dict to map the name of the columns
        # key: column name to be replaced, value: new name of the column
        renamed_columns = {}
        for col_name in columns:
            match = pattern.match(col_name)
            carton_num, unit = match.groups()
            # Get the unit of the current column
            unit = dimension_pattern.sub("", unit)

            if unit in self.data_config["valid_dimensions"]:
                # Get the number related to the current column and subtract 1
                carton_num = int(carton_num) - 1
                new_column_name = f"boxes__{carton_num}__{unit}"
                self.boxes_columns.append(new_column_name)
                # Saves the new names in a list for reordering later
                renamed_columns[col_name] = new_column_name

        return df_base.rename(renamed_columns)

    def create_bullets_columns(self, df_base: pl.DataFrame) -> pl.DataFrame:
        """
        Creates the 'bullets' columns
        """

        # Pattern to get all the "selling point" columns
        regex_str = r"^selling\s*point\s*(\d+)$"
        columns = df_base.select(regex_str).columns
        pattern = re.compile(regex_str)

        # Create a dict to map the name of the columns
        # key: column name to be replaced, value: new name of the column
        renamed_columns = {}
        for col_name in columns:
            match = pattern.match(col_name)
            # Get the number related to the current column and subtract 1
            selling_num = match.groups()[0]
            selling_num = int(selling_num) - 1
            new_column_name = f"product__bullets__{selling_num}"
            # Saves the new names in a list for reordering later
            self.bullets_columns.append(new_column_name)
            renamed_columns[col_name] = new_column_name

        return df_base.rename(renamed_columns)

    def transform_dimensions(self, df_base: pl.DataFrame) -> pl.DataFrame:
        """
        Transform all the columns that constains 'dimensions' keyword.
        Generally these columns comes in the format length x width x height
        but there are edge cases where it has only two dimensions 'length' and 'width'.

        Transforms all columns containing the 'dimensions' keyword.
        Generally, these columns come in the format length x width x height,
        however there are cases where some columns have only two dimensions:
        length and width and need to be treated accordingly.
        """

        # Regex pattern to get all the columns that contains the "dimension" keyword
        columns = df_base.select("^.*dimension.*$").columns
        # Pattern to remove the keyword and characters not related to column name
        col_name_pattern = re.compile(r"dimensions?.*\(\w*\)")
        # Pattern to get the digit, if there is one.
        # There are two cases that need to be dealt with:
        # 1. When the digit comes after the column name .
        # 2. When the digit comes in the middle of the column name.
        digit_pattern = re.compile(r"[^\D]*\d*[^\D]\s*")
        replace_char_pattern = re.compile(r"[-\s_/]")
        df_dimensions = []
        for col in columns:
            # Remove unwanted characters.
            column_name = col_name_pattern.sub("", col).strip()
            # Remove the digits
            column_name = digit_pattern.sub("", column_name).strip()
            # Replace spaces and special characters with "__".
            column_name = replace_char_pattern.sub("__", column_name.strip())

            # Get the column digit.
            dimension_num = re.search(r"\d+", col)
            # As there are columns without digits, it needs to be handled.
            dimension_num = (
                f"{int(dimension_num.group().strip()) - 1}__"
                if dimension_num
                else ""
            )
            # Create the new names for the columns.
            columns_alias = [
                f"{column_name}__{dimension_num}length",
                f"{column_name}__{dimension_num}width",
                f"{column_name}__{dimension_num}height",
            ]

            # There are edges cases with only one dimension, as it's difficult to
            # calculate these dimensions without additional information,
            # it sets them to null.
            df_base = df_base.with_columns(
                pl.when(
                    pl.col(col).str.contains(r"^\d+(\.\d+)?\s*(wide|round)$")
                )
                .then(pl.lit(None))
                .otherwise(pl.col(col))
                .alias(col)
            )
            # Handle the column with only 2 dimensions
            dimensions = 2 if column_name == "furniture__seat" else 3
            columns_alias = columns_alias[:dimensions]
            # Saves the new names in a list for reordering later
            self.dimensions_columns.extend(columns_alias)

            # Split the column by the "x" character then create the columns with their
            # respective dimensions.
            # It creates a new DataFrame for each set of dimensions that has been split,
            # using the "ean13" column as the key, in order to join them later."
            df_dimensions.append(
                df_base.with_columns(
                    pl.col(col)
                    .str.replace(r"[*xX]", "x")
                    .str.split("x")
                    .alias("split_dim")
                )
                .filter(pl.col("split_dim").is_not_null())
                .with_columns(
                    [
                        pl.col("split_dim")
                        .list.get(n)
                        .str.strip()
                        .alias(columns_alias[n])
                        .cast(pl.Float64)
                        for n in range(dimensions)
                    ]
                )
                .drop(["split_dim", col])
                .select(["ean13", *columns_alias])
            )

        # Concatenates the all the "dimensions" DataFrames in the list,
        # using the "ean13" column as the common key for alignment,
        # and join them to the original DataFrame.
        df_dimensions = pl.concat(df_dimensions, how="align")
        self.logger.info(
            f"[TRANSFORM] Created {df_dimensions.shape[1] - 1} "
            "new columns from the dimension columns."
        )
        return df_base.join(df_dimensions, on="ean13", how="left")

    def transform_boolean_columns(self, df_base: pl.DataFrame) -> pl.DataFrame:
        """
        Transforms the columns defined in "boolean_columns" in the config file.
        It changes the values from 'yes' or 'no' to 'true' or 'false' respectively.
        """
        return df_base.with_columns(
            [
                pl.when(pl.col(col).str.to_lowercase() == "yes")
                .then(pl.lit(True))
                .otherwise(pl.lit(False))
                .alias(col)
                for col in self.data_columns["boolean_columns"]
            ]
        )

    @staticmethod
    def handle_missing_weight(df_base: pl.DataFrame) -> pl.DataFrame:
        """
        It looks for missing values in the "weight" column
        in the "boxes__0__weight" column.
        """
        return df_base.with_columns(
            pl.when(pl.col("weight").is_null())
            .then(pl.col("boxes__0__weight"))
            .otherwise(pl.col("weight"))
            .alias("weight")
        )

    def create_unknow_columns(self, df_base: pl.DataFrame) -> pl.DataFrame:
        return df_base.with_columns(
            [
                pl.lit(None).alias(col)
                for col in self.data_columns["unknow_columns"]
            ]
        )

    def reorder_columns(self, df_base: pl.DataFrame) -> pl.DataFrame:
        """
        It rearranges the columns so that the final file has the same order as the
        example provided.
        It gets the "placeholder" columns indexes and replace them with the respective
        columns created in the previous methods.
        """
        placeholders = {
            "boxes_placeholder": self.boxes_columns,
            "bullets_placeholder": self.bullets_columns,
            "dimensions_placeholder": self.dimensions_columns,
        }
        for placeholder, replacement in placeholders.items():
            index = self.data_columns["columns_order"].index(placeholder)
            self.data_columns["columns_order"][index : index + 1] = replacement

        return df_base.select(self.data_columns["columns_order"])
