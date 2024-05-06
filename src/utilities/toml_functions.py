from pytomlpp import load, DecodeError
from os import path


def load_toml_file(toml_file_path: str) -> dict:
    """
    Load toml file and converts it into a dictionary.
    """
    try:
        toml_file = load(toml_file_path)
    except (DecodeError, Exception) as e:
        print(f"[ERROR] Error loading {path.basename(toml_file_path)}: {e}")
        exit()
    return toml_file
