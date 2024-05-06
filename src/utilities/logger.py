import logging
import os
from datetime import datetime
from logging import Logger


def set_logger(path_logger: str) -> Logger:
    """
    Sets the logger configuration
    Parameters
    ----------
    path_logger: str
        The full path where the log file will be saved.

    Returns
    ----------
        The logger object.
    """
    current_day = datetime.now().strftime("%Y_%m_%d")
    path_logger = f"{path_logger}_{current_day}.txt"

    if os.path.isfile(path_logger):
        os.remove(path_logger)

    logger = logging.getLogger(__file__)
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler(path_logger)
    ch = logging.StreamHandler()

    formatter = logging.Formatter("[%(levelname)1s]  %(message)s")
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger
