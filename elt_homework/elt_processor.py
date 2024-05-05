
import logging

import country_converter as coco
import numpy as np
import pandas as pd

from elt_homework.csv_reader import CSVReader
from elt_homework.mapping import columns_mapping, output_columns
from elt_homework.schema import ProductSchema

logger = logging.getLogger(__name__)

cc = coco.CountryConverter()

class ETL:
    def __init__(self):
        self._csv_reader = CSVReader()
    
    def _read_data(self, file_path):
        """
        Reads a CSV file and performs ETL operations with the useful columns
        
        Args:
        - file_path (str): Path to the CSV file.
        """
        logger.info(f'Reading {file_path} file')
        return self._csv_reader.read_csv(file_path, columns_mapping.keys())
   
    def _transformations(self, df):

        def yes_no_to_bool(v):
            if isinstance(v, str):
                return v.lower() == 'yes' 
            return False
        # to bool
        df['attrib__outdoor_safe'] = df['attrib__outdoor_safe'].apply(yes_no_to_bool)
        df['attrib__kit'] = df['attrib__kit'].apply(yes_no_to_bool)
        df['attrib__bulb_included'] = df['attrib__bulb_included'].apply(yes_no_to_bool)
        # to int
        df['attrib__number_bulbs'] = df['attrib__number_bulbs'].fillna(0).astype(int)
        df['product__multipack_quantity'] = df['product__multipack_quantity'].fillna(0).astype(int)
        # to str
        df['ean13'] = df['ean13'].astype(str)
        # contry:
        df['product__country_of_origin__alpha_3'] = cc.pandas_convert( \
             series=df['product__country_of_origin__alpha_3'], to='ISO3',not_found= np.NaN)
        # currency:
        df['cost_price'] = df['cost_price'].replace('[\$,]', '', regex=True).astype(float).round(2)
        
        return df

    def process(self, file_path):
        
        # Read csv from file_path
        df = self._read_data(file_path)
        
        # Rename the columns according to the mapping
        df.rename(columns=columns_mapping, inplace=True)
        
        # Apply the transformations
        df = self._transformations(df)

        try:
            ProductSchema.validate(df)
        except Exception as ex:
        # TODO alert system monitoring,
        #It may be that the supplier/partner has changed something
            raise ex

        # Load all columns
        output_df = pd.DataFrame(columns=output_columns)

        # Fill the blank df columns with the existing data
        for column in df.columns:
            output_df[column] = df[column]
        # Write csv
        output_df.to_csv("output.csv", index=False)

        logger.info(f'ETL finished, {output_df.shape[0]} rows,{output_df.shape[1]} cols saved')


