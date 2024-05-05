import fire
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def run(file_path='homework.csv'):
    """
    Reads the CSV files and performs ETL operation.
    
    Args:
    - file_path (str): Path to the CSV file.
    """
    from elt_homework.elt_processor import ETL 
    logging.info('Starring ETL')
    etl = ETL()
    etl.process(file_path)

if __name__ == '__main__':
   fire.Fire(run)
