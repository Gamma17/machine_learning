# Simple _k_-means
An implementation of [the simple _k_-means clustering algorithm](https://en.wikipedia.org/wiki/K-means_clustering#Standard_algorithm "Wikipedia entry for the standard k-means algorithm") in Python, with a couple of tools for converting [Weka](http://www.cs.waikato.ac.nz/ml/weka/index.html "Weka") ARFF files to Python modules. 

Since Python is a dynamic language, I decided to represent the data directly in a Python module. An example is the module `mlearn.data.iris_numeric`.

__Note:__ this project is based on version 2.7.12 of Python and tested on Linux.

## Running _k_-means
```
usage: python run_kmeans.py [-h] module k max_iterations

Run k-means clustering

positional arguments:
  module          data module
  k               number of clusters
  max_iterations  maximum number of iterations

optional arguments:
  -h, --help      show this help message and exit
```

### Example:
```
python run_kmeans.py mlearn.data.iris_numeric 3 100
```

## Running the ARFF-to-Python converter
As a convenient starting point, I used the [Weka] (http://www.cs.waikato.ac.nz/ml/weka/index.html "Weka") ARFF iris data and converted it to a module. 

* See [ARFF (book version)] (http://weka.wikispaces.com/ARFF+%28book+version%29 "ARFF (book version)")
* Designed to work with the ARFF files distributed with Weka version 3.6.14.
* Supports only numeric and nominal attributes; string, date and relation-valued attributes are not supported.
* It doesn't support missing values, represented in ARFF files by '?'.

```
usage: convert_arff.py [-h] file

Convert Weka ARFF files.

positional arguments:
  file        an ARFF file

optional arguments:
  -h, --help  show this help message and exit
```

### Example:
```
python convert_arff.py arff/iris.arff
```

## Removing attributes from modules
During development, I needed a way to remove attributes from generated modules. For example, I wanted to remove nominal attributes. So, another script:
```
usage: exclude_attributes.py [-h]
                             input_module output_module_name attributes
                             [attributes ...]

Output a new module that excludes specific attributes in the original module.

positional arguments:
  input_module        input data module
  output_module_name  output data module name
  attributes          input data module file

optional arguments:
  -h, --help          show this help message and exit
```

### Example:
```
python exclude_attributes.py mlearn.data.iris iris_numeric class
```

## Run tests
### To run all available tests:
```
python -m unittest discover
```
### To run individual suites:
```
python -m unittest test.test_kmeans
python -m unittest test.test_convert_arff
python -m unittest test.test_filter
```
