import pandas as pd
from typing import Callable

columns_map = {
    "manufacturer_sku":"item number",
    "ean13":"upc",
    "weight":"item weight (pounds)",
    "length":"item depth (inches)",
    "width":"item width (inches)",
    "height":"item height (inches)",
    "prop_65":"",
    "cost_price":"wholesale ($)",
    "min_price":"map ($)",
    "made_to_order":"",
    "product__product_class__name":"item category",
    "product__brand__name":"brand",
    "product__title":"description",
    "product__description":"long description",
    "product__bullets__0":"selling point 1",
    "product__bullets__1":"selling point 2",
    "product__bullets__2":"selling point 3",
    "product__bullets__3":"selling point 4",
    "product__bullets__4":"selling point 5",
    "product__bullets__5":"selling point 6",
    "product__bullets__6":"selling point 7",
    "product__configuration__codes":"",
    "product__multipack_quantity":"",
    "product__country_of_origin__alpha_3":"country of origin",
    "product__parent_sku":"",
    "attrib__arm_height":"",
    "attrib__assembly_required":"",
    "attrib__back_material":"",
    "attrib__blade_finish":"",
    "attrib__bulb_included":"bulb 1 included",
    "attrib__bulb_type":"bulb 1 type",
    "attrib__color":"",
    "attrib__cord_length":"cord length (inches)",
    "attrib__design_id":"",
    "attrib__designer":"",
    "attrib__distressed_finish":"",
    "attrib__fill":"",
    "attrib__finish":"item finish",
    "attrib__frame_color":"",
    "attrib__hardwire":"",
    "attrib__kit":"",
    "attrib__leg_color":"",
    "attrib__leg_finish":"",
    "attrib__material":"item materials",
    "attrib__number_bulbs":"Bulb 1 count",
    "attrib__orientation":"",
    "attrib__outdoor_safe":"",
    "attrib__pile_height":"",
    "attrib__seat_depth":"",
    "attrib__seat_height":"",
    "attrib__seat_width":"",
    "attrib__shade":"",
    "attrib__size":"",
    "attrib__switch_type":"",
    "attrib__ul_certified":"",
    "attrib__warranty_years":"",
    "attrib__wattage":"",
    "attrib__weave":"",
    "attrib__weight_capacity":"",
    "boxes__0__weight":"carton 1 weight (pounds)",
    "boxes__0__length":"carton 1 length (inches)",
    "boxes__0__height":"carton 1 height (inches)",
    "boxes__0__width":"carton 1 width (inches)",
    "boxes__1__weight":"carton 2 weight (pounds)",
    "boxes__1__length":"carton 2 length (inches)",
    "boxes__1__height":"carton 2 height (inches)",
    "boxes__1__width":"carton 2 width (inches)",
    "boxes__2__weight":"carton 3 weight (pounds)",
    "boxes__2__length":"carton 3 length (inches)",
    "boxes__2__height":"carton 3 height (inches)",
    "boxes__2__width":"carton 3 width (inches)",
    "boxes__3__weight":"",
    "boxes__3__length":"",
    "boxes__3__height":"",
    "boxes__3__width":"",
    "product__styles":"item style"
}

class Mapper:
    """This class will hadle the creation of a mapper which will allow to map fields from one file to another.
    """

    def __init__(self,mapper_dict:dict=columns_map) -> None:
        """
        Initializes the Mapper with an optional dictionary that maps fields from one file to another.

        Args:
            mapper_dict (dict): A dictionary that maps field names. Defaults to `columns_map`.

        Returns:
            None

        Raises:
            AssertionError: If `mapper_dict` is not a dictionary.
        """

        if isinstance(mapper_dict,dict):
            self.fields_map = mapper_dict.copy()
        else:
            raise AssertionError('Only dict data type is accepted.')
    
    def create(self, key:str, value:str) -> None:
        """
        Creates a new mapping in the Mapper.

        Args:
            key (str): The field to be in the final frame.
            value (str): The field that already exists and needs to be changed.

        Returns:
            None

        Raises:
            AssertionError: If `key` or `value` is not a string. If the `key` already exists, use the `update` method instead.
        """
        if not isinstance(key,str) or not isinstance(value,str):
            raise AssertionError("Check key, value data type, only strings are allowed.")
        if key not in self.fields_map.keys():
            self.fields_map[key] = value
        else:
            raise AssertionError('Use update method for existing keys.')
    
    def update(self,key:str,value:str) -> None:
        """
        Updates an existing mapping in the Mapper.

        Args:
            key (str): The field to be in the final frame.
            value (str): The field that already exists and needs to be changed.

        Returns:
            None

        Raises:
            AssertionError: If `key` is not a string. If the `key` does not exist, use the `create` method instead.
        """
        if not isinstance(key,str) or not isinstance(value,str):
            raise AssertionError("Check key data type, only strings are allowed.")
        if key in self.fields_map.keys():
            self.fields_map[key] = value
    
    def delete(self,key:str)-> None:
        """
        Deletes a mapping from the Mapper.

        Args:
            key (str): The field name to delete.

        Returns:
            None

        Raises:
            AssertionError: If `key` is not a string. If the `key` does not exist, it will be silently ignored.
        """
        if not isinstance(key,str):
            raise AssertionError("Check key, value data type, only strings are allowed.")
        if key in self.fields_map:
            self.fields_map.pop(key)



class DataTransformer:

    def __init__(self, path_to_file:str="homework.csv", mapper:Mapper=Mapper())-> None:
        """
        Initializes the DataTransformer with an optional CSV file path and a Mapper object.

        Args:
            path_to_file (str): The path to the CSV file. Defaults to "homework.csv".
            mapper (Mapper): A Mapper object. Defaults to a new instance of Mapper().

        Returns:
            None

        Raises:
            FileNotFoundError: If the file specified by `path_to_file` doesn't exist.
            AssertionError: If `mapper` is not an instance of `Mapper`.

        Notes:
            - Make sure the file exists and is readable before calling this method.
        """

        self.initial_frame = pd.read_csv(path_to_file, dtype=str)
        self.transformations = {}
        if not isinstance(mapper,Mapper):
            raise AssertionError('Only the class Mapper is allowed to work as mapper. Avoid any other class or data type')
        self._mapper = mapper
    
    def register_transformation(self, key:str, transformer:Callable)-> None:
        """Method to register custom transformation to apply in a declared field.

        Args:
            key (str): Field objective to be transformed
            transformer (Callable): function who performs the transformation
        Returns:
            None

        Raises:
            AssertionError: If `transformer` is not a callable or if `key` is not a valid field in the mapper.
        """
        if callable(transformer) and key in self._mapper.fields_map.keys():
            self.transformations[key] = transformer
        else:
            raise AssertionError('Only functions are allowed to be passed as transformers. Only existing fields in the mapper are allowed.')
        
    def filter_columns(self)-> None:
        """Method to extract the columns from initial_frame to create final_frame and rename those columns, based on
        the mapper. It will also add columns empty for those fields with no field map.

        If the filtered dataframe is empty, it will stay like that.

        Returns:
            None  
        """
        columns_to_filter = [col for col in self._mapper.fields_map.values() if col in self.initial_frame.columns]
        self.final_frame = self.initial_frame.loc[:,columns_to_filter]

        if not self.final_frame.empty:
            self.final_frame = self.final_frame.rename(columns={value:key for key,value in self._mapper.fields_map.items()})
            missing_columns = self._mapper.fields_map.keys() - self.final_frame.columns
            for column in missing_columns:
                self.final_frame[column] = ''

            self.final_frame = self.final_frame.loc[:,list(self._mapper.fields_map.keys())]        
    
    def apply_transformations(self)-> None:
        """Iterate over the transformations and apply to each value the designed transformation function.

        Returns:
            None
        """
        for column, transformer in self.transformations.items():
            self.final_frame[column] = self.final_frame[column].apply(lambda x:transformer(x))
    
    def dump_frame(self,filename:str='formatted.csv') -> None:
        """
        Dumps the transformed data frame to a CSV file.

        Args:
            filename (str): The name of the output CSV file. Defaults to "formatted.csv".

        Returns:
            None
        """
        self.final_frame.to_csv(filename, index=False)