<h1>ETL Service</h1>
<h2>Overview</h2>
<p>This Python project implements an Extract, Transform, Load (ETL) service that processes data from CSV files. It reads data from an input CSV file, applies transformations based on specified rules, and then writes the transformed data to an output CSV file.</p>
<h2>Features</h2>
<ul>
    <li>Reads CSV files containing raw data.</li>
    <li>Transforms the data according to predefined rules.</li>
    <li>Writes the transformed data to a new CSV file.</li>
    <li>Supports various transformations such as date format conversion, currency rounding, and unit conversion.</li>
    <li>Code coverage at 93% you can run unit tests with pytest and coverage: <code>coverage run -m pytest .</code>.</li>
</ul>
<h2>How to Use</h2>
<h3>Usage</h3>
<ol>
    <li><p>Prepare your input CSV file containing the raw data to be processed.</p></li>
    <li><p>Define a columns mapping file in JSON format. This file specifies how each column in the input file should be transformed. An example columns mapping file might look like this:</p></li>
</ol>

```json
{
    "system creation date": "date",
    "wholesale ($)": "wholesale_price",
    "item width (cm)": "width_inches",
    "item length (feet)": "length_inches",
    "item weight (kg)": "weight_pounds",
    "upc": "upc_code"
}
```
<ol start="3"><li>Run the ETL service using the following command:</li></ol>
<pre><code>python main.py input.csv output.csv columns_mapping.json
</code></pre>

<p>Replace <code>input.csv</code> with the path to your input CSV file, <code>output.csv</code> with the desired path for the output CSV file, and <code>columns_mapping.json</code> with the path to your columns mapping file.</p>

<ol start="4"><li>Once the process completes, you will find the transformed data written to the specified output CSV file.</li></ol>
<h2>Example</h2>
<p>Let's say we have an input CSV file <code>data.csv</code> containing the following data:</p>

| system creation date | wholesale ($) | item width (cm) | item length (feet) | item weight (kg) | upc         |
|----------------------|---------------|------------------|---------------------|-------------------|-------------|
| 7/7/15               | $10.50        | 20               | 2                   | 2.1               | 123456789012|


<p>And a columns mapping file <code>columns_mapping.json</code> as shown above.</p>
<p>Running the ETL service with the following command:</p>
<pre><code>python main.py data.csv transformed_data.csv columns_mapping.json
</code></pre>
<p>Will result in a new CSV file <code>transformed_data.csv</code> with the following data:</p>

| date       | wholesale_price | width_inches | length_inches | weight_pounds | upc_code    |
|------------|-----------------|--------------|---------------|---------------|-------------|
| 2015-07-07 | 10.50           | 7.87         | 24            | 4.62          | 123456789012|

