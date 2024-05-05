import logging
import pandas as pd

logger = logging.getLogger(__name__)

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
            return pd.read_csv(file_path, usecols=columns, engine='python')
        except Exception as e:
            logger.exception("An error occurred:", e)
            
    
            