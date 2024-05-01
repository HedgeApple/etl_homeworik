
from elt_homework.csv_reader import CSVReader 

class ETL:
    def __init__(self):
        self._csv_reader = CSVReader()
        
        self._data = None
        self._columns = None
    
    def _read_data(self, file_path, cols_file_path):
        """
        Reads a CSV file and performs ETL operations.
        
        Args:
        - file_path (str): Path to the CSV file.
        """
        self._data = self._csv_reader.read_csv(file_path)
        
        self._columns = self._csv_reader.get_column_names(cols_file_path)
        
        if self._data is not None:
            # Perform ETL operations here if needed
            print("Data loaded successfully.")
            print(self._data.head())
            print(self._columns)
        else:
            print("Failed to load data.")

    def process(self, file_path, cols_file_path):
        
        self._read_data(file_path, cols_file_path)
