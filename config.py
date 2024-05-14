"""
Config settings for the entire script.
Eases the process of adjusting properties and changing resources for the script.
Properties include:
    - Filenames: Set defaults for input and output files, and paths to resources and output destination.
    - Enumerations for metrics: Add / remove based on what can be expected.
    - Regex Strings: Quickly edit and correct when edge cases are discovered.
"""

# Python Built-In Imports
from enum import Enum
from json import load
from os import getcwd
from os.path import join
from typing import Dict

RESOURCE_DIR = "resources"
"Name of the directory where resources are contained."

def get_resource_path(filename: str) -> str:
    "Returns the full path to the file within the directory specified by RESOURCE_DIR"
    return join(getcwd(), RESOURCE_DIR, filename)

OUTPUT_DIR = "output"
"Name of the directory where results / output are placed saved."

def get_output_path(filename: str) -> str:
    "Returns the full path to the file within the directory specified by OUTPUT_DIR"
    return join(getcwd(), OUTPUT_DIR, filename)

DEF_INPUT_FILENAME = "homework.csv"
"Name of the default input file."

DEF_INPUT_PATH = get_resource_path(DEF_INPUT_FILENAME)
"Full path to the default input file."

DEF_OUTPUT_FILENAME = "formatted.csv"
"Name of the default output file."

DEF_OUTPUT_PATH = get_output_path(DEF_OUTPUT_FILENAME)
"Full path to the default output file."

ALPHA_3_FILENAME = "alpha_3_codes.json"
"Name of the file containing the country name to alpha 3 mapping."

ALPHA_3_PATH = get_resource_path(ALPHA_3_FILENAME)
"Full path to the file containing the country name to alpha 3 mapping."

ALPHA_3 = {}
"Dictionary mapping country names to their alpha 3 codes."

with open(ALPHA_3_PATH, 'r') as alpha3_json: # Load alpha 3 resource
    ALPHA_3: Dict[str, str] = load(alpha3_json)

class WeightMetric(Enum):
    "Enumerate metrics of weight that are reasonable for furniture."
    
    t = 1
    "Metric Tonne (t)"

    kg = 2
    "Kilogram (kg)"

    g = 3
    "Gram (g)"

    lb = 4
    "Pound (lb)"
    oz = 5
    "Ounce (oz)"

class DistanceMetric(Enum):
    "Enumerate metrics of distance that are reasonable for furniture."

    cm = 1
    "Centimeter (cm)"

    m = 2
    "Meter (m)"

    inch = 3 # Would shorten to in, but that's a keyword.
    "Inch (in)"

    ft = 4
    "Foot (ft)"

    yd = 5
    "Yard (yd)"

class RegexStrings:
    "Store quick references to regex strings with names that describe what they match."

    REAL_POS = "^(\d*\.)?\d+$"
    "Matches any positive real number (Ex: 123, 1.234, .1230)."

    SHORT_SET = "/S(\d+)"
    "Regex string for capturing set size from item number."

    SET_NUMS = ["set/(\d+)", "set of[\s*](\d+)", "(\d+)-pack"]
    "List of regex strings that can denote the number of products in a set in an item's short or long descriptions."
        