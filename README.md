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


## Solution

For this project, there's a main function that calls the Transform function, each line corrrespond to one "transformation". Different steps are considered since multiple updates are required. 
At a high level, the steps are the following:
1. Read the csv files
2. Rename columns according to a mapping (please check utility file where helpers are located)
3. Countries are transformed into alpha3 (requirements.txt includes the library to do so)
4. Datatype transformation, where mostly datatypes are corrected, missing values are filled and more.
5. Added new columns to match the expected format for the output file
6. EAN13 column, needed a specific formatting so I added this here, it can be improved to be included within the datatype transformation method.

As a final step, it generates a csv in the same working directory as the input files called "formatted.csv" with the output data.