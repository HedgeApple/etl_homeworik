# Task

1. Fork this project
2. Create a python script that reads all of the rows from `homework.csv` and outputs them to a new file `formatted.csv` using the headers from `example.csv` as a guideline.  (See `Transformations` below for more details.)
3. You may you any libraries you wish, but you must include a `requirements.txt` if you import anything outside of the standard library.
4. There is no time limit for this assignment.
5. You may ask any clarifying questions via email.
6. Create a pull request against this repository with an English description of how your code works when you are complete

## Transformations

Follow industry standards for each data type when decided on the final format for cells.

* Dates should use ISO 8601
* Currency should be rounded to unit of accounting. Assume USD for currency and round to cents.
* For dimensions without units, assume inches. Convert anything which isn't in inches to inches.
* For weights without units, assume pounds. Convert anything which isn't in pounds to pounds.
* UPC / Gtin / EAN should be handled as strings
* Floating point and decimal numbers should preserve as much precision as possible

# Solution
## Idea
The idea behind this implementation is that any part of the code can be used to analize others files.
* The mapper can be changed totally to map new files, or can me modified a little by the methods.

* The `DataTransformer` class will handle the transformation over the dataframes and will hold the changes for each column based on the transformations registered.

* Each transformation was created as a function with an argument due to the imprevisibility of the change itself, so this way any column can be transformed with a custom converter.

## Usage/Examples

The whole project use the library pandas, which read all the data as string.
A requeriments.txt was added to handle the dependencies(pandas install several dependencies).

The workflow as it can be seen in the project is:
1. Create an instance of a `DataTransformer`. It will manage by default the parameters.
2. Register into the instance created before the transformations.
3. Clean the dataframe and prepare it for the transformation with the method `filter_columns`.
4. Apply the transformations with `apply_transformations`
5. Dump the final dataframe to .csv

### Mapper class

The mapper class is a mapper for the columns required and given respectively. It can be changed to another whole set of columns to be adaptable to new files.
It implements methods for create, delete and update the fields in the mapper.

### Transformations

Due to the particularity of this project the next converters were created as functions:
* ean13_converter
* price_converter
* bool_true_converter
* bool_false_converter

For dimension, weights and datetimes no converters were created, in case that the files change and a new column needs to be transformed (from centimeters, meters, kilometers, kilograms, tons, etc), it can be created and passed into the `DataTransformer.register_transformation` method.

A self discover method to transform the data is not implemented because what will determinate the conversion is the unit in the header and is not clear until the file is particulary analized.


## Running Tests

To run tests, run the following command

```bash
  pytest
```