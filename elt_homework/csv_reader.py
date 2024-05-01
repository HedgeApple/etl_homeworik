import pandas as pd

class CSVReader:
    def __init__(self):
        pass
    
    def read_csv(self, file_path):
        """
        Reads a CSV file using pandas.
        
        Args:
        - file_path (str): Path to the CSV file.
        
        Returns:
        - DataFrame: The DataFrame containing the CSV data.
        """
        try:
            data = pd.read_csv(file_path)
            return data
        except FileNotFoundError:
            print("File not found.")
            return None
        except Exception as e:
            print("An error occurred:", e)
            return None
        
    def get_column_names(self, file_path):
        """
        Returns the column names from a CSV file.
        
        Args:
        - file_path (str): Path to the CSV file.
        
        Returns:
        - list: List of column names.
        """
        try:
            data = pd.read_csv(file_path, nrows=1)
            return data.columns.tolist()
        except FileNotFoundError:
            print("File not found.")
            return None
        except Exception as e:
            print("An error occurred:", e)
            return None