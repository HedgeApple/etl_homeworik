import csv
import json
from typing import Any, List
import pytest

from etl import ETLService


@pytest.fixture
def etl_instance():
    """Fixture for instantiating the ETL class."""
    return ETLService()

def test_run(etl_instance):

    etl_instance.run('homework.csv', 'test_run.csv', 'columns_mapping.json')

    data: List[List[Any]] = []

    with open('test_run.csv', 'r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            data.append(row)

    assert len(data) == 6671

def test_read_csv(etl_instance):

    with open('test_read.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['iso date'])
        writer.writerows([['2015-07-07']])

    input_data = etl_instance.read_csv('test_read.csv')

    assert input_data == [['iso date'], ['2015-07-07']]


def test_write_csv(etl_instance):
    input_data = [
        ['07/07/15'],
    ]
    etl_instance.columns_mapping = {
        "system creation date": "iso date",
    }
    etl_instance.input_file_headers = ['system creation date']

    etl_instance.output_file_headers = [column for column in etl_instance.columns_mapping.values() if column is not None]
    
    # Call the transform_data method
    transformed_data = etl_instance.transform_data(input_data)

    etl_instance.write_csv('new.csv', transformed_data)

    data: List[List[Any]] = []

    with open('new.csv', 'r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            data.append(row)

    assert data == [['iso date'], ['2015-07-07']]

def test_transform_data_homework_file(etl_instance):
    input_data = etl_instance.read_csv('homework.csv')

    input_data = etl_instance.extract_headers(input_data)
    
    with open('columns_mapping.json', 'r') as f:
        etl_instance.columns_mapping = json.load(f)

    # Call the transform_data method
    transformed_data = etl_instance.transform_data(input_data)

    # Verify that the result has the same number of rows as the input data
    assert len(transformed_data) == len(input_data)

    # Verify that currency values are rounded correctly
    assert transformed_data[0][2] == "228.00"
    assert transformed_data[6618][2] == "337.00"

def test_transform_data(etl_instance):
    # Example input data
    input_data = [
        ['7/7/15', '10', '8', '2.1'],
        ['7/7/16', '21', '', '4.5']
    ]
    etl_instance.columns_mapping = {
        "system creation date": "iso date",
        "width (feet)": "width (inches)",
        "height (cm)": "height (inches)",
        "weight (kg)": "weight (pounds)"
    }
    etl_instance.input_file_headers = ['system creation date', 'width (feet)', 'height (cm)', 'weight (kg)']

    # Call the transform_data method
    transformed_data = etl_instance.transform_data(input_data)

    # Verify that the result has the same number of rows as the input data
    assert len(transformed_data) == len(input_data)

    # Verify that currency values are rounded correctly
    assert transformed_data[0][0] == '2015-07-07'
    assert transformed_data[1][0] == '2016-07-07'

    # feet to inches
    assert transformed_data[0][1] == '120.0'
    assert transformed_data[1][1] == '252.0'

    # centimeters to inches
    assert transformed_data[0][2] == '3.15'
    assert transformed_data[1][2] == ''

    # kg to pounds
    assert transformed_data[0][3] == '4.63'
    assert transformed_data[1][3] == '9.92'

def test_transform_data_date_error(etl_instance):
    # Example input data
    input_data = [
        ['07-07-15'],
    ]
    etl_instance.columns_mapping = {
        "system creation date": "iso date",
    }
    etl_instance.input_file_headers = ['system creation date']

    # Call the transform_data method
    transformed_data = etl_instance.transform_data(input_data)

    # Verify that the result has the same number of rows as the input data
    assert len(transformed_data) == len(input_data)

    # Verify that currency values are rounded correctly
    assert transformed_data[0][0] == '07-07-15'
