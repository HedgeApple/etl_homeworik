import sys
from typing import List, Any

from etl import ETLService


def main() -> None:

    if len(sys.argv) != 4:
        print("Use: python main.py <input_file> <output_file> <mapping_file>")
        sys.exit(1)

    input_file: str = sys.argv[1]
    output_file: str = sys.argv[2]
    columns_mapping_file: str = sys.argv[3]

    ETLService().run(input_file, output_file, columns_mapping_file)

if __name__ == "__main__":
    main()
