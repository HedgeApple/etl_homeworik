import polars as pl
from glob import glob
from os import path
from logging import Logger

current_file_dir = path.dirname(path.realpath(__file__))


class Extract:
    def __init__(self, config: dict, logger: Logger) -> None:
        self.logger = logger
        self.root_folder = path.dirname(path.dirname(current_file_dir))
        self.data_file_source = config["data_file_source"]
        self.data_file_output = config["data_file_output"]
        self.data_columns = config["data_columns"]

    def load_file(self) -> pl.DataFrame:
        """
        Loads data from the directory path.
        It can handle multiple files as long they are in the same format
        and specified on the configuration file.
        """

        # To handle other file formats, specify it in the configuration file
        if self.data_file_source["file_extension"] == ".csv":
            file_path = path.join(
                self.root_folder,
                self.data_file_source["file_path"],
                self.data_file_source["file_name"],
            )

            files_to_read = glob(file_path)
            self.logger.info(
                f"[LOADER] Starting reading files from: {file_path}."
            )
            self.logger.info(
                f"[LOADER] Found {len(files_to_read)} file(s) to read."
            )

            # With the scan_csv we Lazy read the file to increase performance and
            # reduce memory overhead.
            # This behavior is easier to notice when reading several files
            # or very large files
            # For more information please read the docs:
            # https://docs.pola.rs/user-guide/concepts/lazy-vs-eager/
            # https://docs.pola.rs/user-guide/lazy/using/
            df_list = [
                pl.scan_csv(
                    file,
                    separator=self.data_file_source["file_separator"],
                    encoding=self.data_file_source["file_encoding"],
                    infer_schema_length=0,
                ).drop(self.data_columns["useless_columns"])
                for file in files_to_read
            ]

            self.logger.info("[LOADER] File(s) read successfully.")
            return pl.concat(df_list).collect()

    def save_file(self, df_base: pl.DataFrame) -> None:
        """
        Saves the final data in the path defined in the configuration file.
        Parameters
        ----------
        df_base
            The data formatted and parsed.
        """
        if self.data_file_output["file_extension"] == ".csv":
            self.logger.info("[LOADER] File will be saved in CSV format.")

            file_name = f"{self.data_file_output['file_name']}{self.data_file_output['file_extension']}"
            file_path_output = path.join(
                self.root_folder,
                self.data_file_output["file_path"],
                file_name,
            )

            df_base.write_csv(
                file_path_output,
                separator=self.data_file_output["file_separator"],
            )
            self.logger.info(
                "[LOADER] File saved successfully on the path:"
                f" {file_path_output}"
            )
