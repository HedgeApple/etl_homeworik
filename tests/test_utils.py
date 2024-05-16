from ..utils import Mapper, columns_map, DataTransformer
import pytest
import pandas as pd

def test_mapper_class_has_default_mapper_dict():
    """The Mapper class could be initialize empty or with a new mapper dict.

    This will test that.
    """
    mapper = Mapper()
    assert mapper.fields_map == columns_map

def test_mapper_accepts_new_mapper_dict():
    """If the user define a new mapper and is passed into the constuctor, this needs to be used.
    """
    new_mapper = {"field_1":"field_1"}
    mapper = Mapper(mapper_dict=new_mapper)
    assert mapper.fields_map == new_mapper

def test_mapper_only_accepts_dict_instance_on_creation():
    """If the user tries to use a list, tuple or another type to pass into the constructor a Assertion error must be raised
    """
    new_mapper = []
    with pytest.raises(AssertionError):
        mapper = Mapper(mapper_dict=new_mapper)
    
    new_mapper = ()
    with pytest.raises(AssertionError):
        mapper = Mapper(mapper_dict=new_mapper)
    
    new_mapper = 'word'
    with pytest.raises(AssertionError):
        mapper = Mapper(mapper_dict=new_mapper)

def test_mapper_can_create_new_key_value_pair():
    """If the script needs to use de default dict or another dict but also needs to add a new pair (key,value)
    the mapper should have a method to handle that.
    """

    mapper = Mapper()
    mapper.create(key="New field",value="Old field")
    columns_map["New field"] = "Old field"
    assert mapper.fields_map == columns_map

def test_mapper_only_create_fields_that_are_not_present():
    """If the field is present in the dict, the method won't change the field and also will raise an AssertionError.
    """
    mapper = Mapper()
    with pytest.raises(AssertionError):
        mapper.create(key="manufacturer_sku",value="Old field")

def test_mapper_only_create_fields_when_key_value_are_strings():
    """Only strings are data type admitted to the create method, otherwise and AssertionError will be raised.
    """
    mapper = Mapper()
    with pytest.raises(AssertionError):
        mapper.create(key="New Field",value=55)
    
    with pytest.raises(AssertionError):
        mapper.create(key=55,value="New Field")
    
def test_mapper_has_update_method():
    """The mapper should have a update method to allow the user to update only a key,value pair in case that is requiered.
    """

    mapper = Mapper()
    mapper.update(key="manufacturer_sku",value="New Value")
    columns_map["manufacturer_sku"] = "New Value"
    assert mapper.fields_map == columns_map

def test_mapper_update_method_only_work_on_existing_keys():
    """If the key passed into the method is not in the fields_map, then the update is ignored.
    """

    mapper = Mapper()
    mapper.update(key="manufacturer_sku",value="New Value")
    columns_map["manufacturer_sku"] = "New Value"
    assert mapper.fields_map == columns_map

def test_mapper_only_update_fields_when_key_value_are_strings():
    """Only strings are data type admitted to the update method, otherwise and AssertionError will be raised.
    """
    mapper = Mapper()
    with pytest.raises(AssertionError):
        mapper.update(key="manufacturer_sku",value=55)
    
    with pytest.raises(AssertionError):
        mapper.update(key=55,value="New Field")

def test_mapper_has_delete_method():
    """The mapper should have a method to delete pairs key,value in case that is requested by the user.
    """
    mapper = Mapper()
    mapper.delete(key="manufacturer_sku")
    columns_map.pop("manufacturer_sku")
    assert columns_map == mapper.fields_map

def test_mapper_ignore_inexisting_keys():
    """If the key to delete doesn't exists, the action will be ignored.
    """
    mapper = Mapper()
    mapper.delete(key="Another Field")
    assert columns_map == mapper.fields_map

def test_delete_only_accepts_strings():
    """Only strings are allowed to be passed as value in the method, otherwise it will raise AssertionError
    """
    mapper = Mapper()
    with pytest.raises(AssertionError):
        mapper.delete(key=55)

#---------------------------------------- Test DataTransformer---------------------------------

def test_data_transformer_has_default_path_to_csv():
    """The class should have a default -path_to_file- so it can be imported to any folder and automatically use that file.
    """
    obj = DataTransformer()
    frame = pd.read_csv('./homework.csv', dtype=str)
    assert frame.equals(obj.initial_frame)

def test_data_transformer_allows_change_in_path_to_csv():
    """Also the class must allows to change the path_to_file
    """
    obj = DataTransformer(path_to_file="./example.csv")
    frame = pd.read_csv('./example.csv', dtype=str)
    assert frame.equals(obj.initial_frame)

def test_data_transformer_creates_empty_transformation_dict():
    """The dict will be used to hold the transformation for each field
    """
    obj = DataTransformer()
    assert obj.transformations == {}

def test_data_transformer_saves_mapper():
    """Initializing the class should create by default a instance of a Mapper if this is not passed as argument.
    """
    obj = DataTransformer()
    assert isinstance(obj._mapper,Mapper)

def test_data_transformer_only_allows_mapper_isntances():
    """Initializing the class should create by default a instance of a Mapper if this is not passed as argument.
    """
    with pytest.raises(AssertionError):
        obj = DataTransformer(mapper={})

def test_data_transformar_has_method_to_register_transformation():
    """The class needs a way to store some custom transformations mapping a field to transform and a custom function to make the transformation
    this will be implemented by a dict like:
            {'field to transform':function}
    """
    def new_function():
        pass
    obj = DataTransformer()
    obj.register_transformation('manufacturer_sku',new_function)
    assert obj.transformations.get('manufacturer_sku') == new_function

def test_data_transformer_prevent_add_a_non_function_to_the_registry():
    """The method should prevent the adition of a non function to the registry, if that is the case and AssertionError will be raised.
    """
    obj = DataTransformer()
    with pytest.raises(AssertionError):
        obj.register_transformation('Field to change','data')

def test_data_transformer_prevent_add_a_non_existing_field_to_the_registry():
    """The method should prevent the adition of a field that is not present in the mapper.
    """
    def new_function():
        pass
    obj = DataTransformer()
    with pytest.raises(AssertionError):
        obj.register_transformation('Field to change',new_function)

def test_data_transformer_filter_columns():
    """The class must have a method to filter the columns of the initial_frame to create the final_frame based on
    the columns in the mapper.
    """
    mapper = Mapper(mapper_dict={'A':'item number','B':'upc'})
    obj = DataTransformer(mapper=mapper)
    obj.filter_columns()
    assert list(obj.final_frame.columns) == ['A','B']


def test_data_transformer_return_empty_dataframe_is_no_columns_are_present():
    """If the columns in the mapper are not present in the initial_frame, the final_frame should be empty.
    """
    mapper = Mapper(mapper_dict={'A':'Data','B':'Data2'})
    obj = DataTransformer(mapper=mapper)
    obj.filter_columns()
    print(obj.final_frame.head(), len(obj.final_frame))
    assert obj.final_frame.empty

def test_data_transformer_has_a_way_to_transform_colums():
    """Each column inside the transformers dict should be transformed into something new, based on the transformer registered.
    """
    def pass_to_1(value):
        return 1
    mapper = Mapper(mapper_dict={'manufacturer_sku':'item number','ean13':'upc'})
    obj = DataTransformer(mapper=mapper)
    obj.register_transformation('manufacturer_sku', pass_to_1)
    obj.filter_columns()
    obj.apply_transformations()
    assert obj.final_frame.iloc[0,0] == 1
    assert obj.final_frame.iloc[1,0] == 1

