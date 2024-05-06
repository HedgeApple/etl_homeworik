from os import path
from time import time

from etl.extract import Extract
from etl.transform import Transform
from etl.normalizer import Normalizer
from utilities.toml_functions import load_toml_file
from utilities.logger import set_logger


current_file_dir = path.dirname(path.realpath(__file__))
toml_file_path = path.join(current_file_dir, "etl", "elt_config.toml")
path_logger = path.join(current_file_dir, "logs", "etl")


def pipeline():
    config = load_toml_file(toml_file_path)
    logger = set_logger(path_logger)

    logger.info("[PIPELINE] Starting ETL pipeline.")
    start_time = time()
    extract = Extract(config, logger)
    df_base = extract.load_file()

    logger.info("[PIPELINE] Starting the normalization of the data.")
    df_base = Normalizer(config, logger).execute(df_base)
    logger.info("[PIPELINE] Starting the transformation of the data.")
    df_base = Transform(config, logger).execute(df_base)
    end_time = time()
    logger.info(f"[PIPELINE] Completed in {end_time - start_time:.2f} minutes.")

    extract.save_file(df_base)
    logger.info(
        "[PIPELINE] The full log of the execution can be found at: src/logs/"
    )


pipeline()
