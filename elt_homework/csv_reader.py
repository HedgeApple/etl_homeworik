import pandas as pd

class CSVReader:
    def __init__(self):
        pass
    
    def read_csv(self, file_path, columns):
        """
        Reads a CSV file using pandas.
        
        Args:
        - file_path (str): Path to the CSV file.
        - columns (list): List of only columns to load
        
        Returns:
        - DataFrame: The DataFrame containing the CSV data.
        """
        try:
            data = pd.read_csv(file_path, usecols=columns, engine='python')
            return data
        except Exception as e:
            print("An error occurred:", e)
            
    
            