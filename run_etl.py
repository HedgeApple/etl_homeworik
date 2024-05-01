import fire

def run(file_path='homework.csv', cols_file_path='example.csv'):
    """
    Reads the CSV files and performs ETL operation.
    
    Args:
    - file_path (str): Path to the CSV file.
    - file_path (str): Path to the CSV columns file.
    """
    from elt_homework.elt_processor import ETL 
    
    etl = ETL()
    etl.process(file_path, cols_file_path)

if __name__ == '__main__':
   run()
