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

## Run ETL

### Requirements
- Python 3.10 

### Install dependencies

```bash
pip install -r requirements.txt 
```
### Usage

```
python3 run_etl.py 
```
#### Can pass the filepath
```
python3 run_etl.py filepath
```