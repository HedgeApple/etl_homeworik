### Project Structure
```
src/
├─ data/
│  ├─ __init__.py
│  ├─ homework.csv
├─ etl/
│  ├─ __init__.py
│  ├─ elt_config.toml
│  ├─ extract.py
│  ├─ normalizer.py
│  ├─ transform.py
├─ logs/
│  ├─ etl_2024_05_06.txt
├─ output/
│  ├─ formatted.csv
├─ utilities/
│  ├─ __init__.py
│  ├─ logger.py
│  ├─ toml_functions.py
│  ├─ units_converter.py
```
### Python version
This solution was made using python version >= 3.12

### Installing the dependencies.
Make sure you are in the root folder.
```bash
pip install -r requirements.txt
```
Next run the script
```bash
python src/pipeline.py
```
<br>
There is also a Dockerfile and a docker-compose configuration. <br>
To run it, just copy/paste the command below into the terminal.

```bash
docker-compose up -d
```

The final data will be in the following directory `src/output` <br>
You can also check the logs on: `src/logs`

## The solution
The code was created using the polars library and the toml config file.
All methods and functions have docstring and are documented.
The code has been designed to deal with as many different situations as possible, 
although it is not possible to predict all the situations, some can be deduced from 
our experience.

### Adjusting the config file.
In the dir `src/etl` you cand find the file `elt_config.toml`.
This configuration was created to abstract some code delegations, such as file format, file extension, 
columns to be renamed, column order, units to be converted, etc.
This way, we can add data-related changes with minimal changes to the code.

#### The Extract class:
The class has two methods: one to read all the files in the `src/data` directory, 
as long as they are in the same format and the second one to save the final data to 
the `src/output`.

#### The Normalizer class:
1. Converts all the columns that are not in the standard unit format: 
 - from centimeter, meter and feet to inches
 - from grams, kilograms and once to pounds.
2. Converts all units to float for maximum precision
3. Converts currency columns to standard format: e.g $2.54
4. Filters null upcs.
5. Converts upc column to ean13 standard.
6. Converts the country columns to alpha_3 standard.
7. Formats the date column to ISO 8601 standard.

#### The Transformer class:
1. Creates the column 'prop65', which is related to Proposition 65.
2. Creates the 'design_id' column.
3. Creates the 'ul_certified' column.
4. Creates the 'product_styles' column.
5. Creates the 'product__parent_sku' column.
6. Creates the 'attrib__number_bulbs' column.
7. Creates the 'boxes' columns dynamically.
8. Creates the 'bullets' columns dynamically.
9. Transform all the dimension columns.
10. Transform all the columns with values 'yes' or 'no' to 'true' or 'false' respectively.
11. Finnaly rearranges the columns so that the final file has the same order as the example provided.
