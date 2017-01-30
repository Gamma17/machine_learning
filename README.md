# Simple _k_-means
An implementation of the simple _k_-means clustering algorithm in Python. 

Since Python is a dynamic language, I decided to represent the data directly in a Python module. An example is the module mlearn.data.iris_numeric.

## Running _k_-means
```
usage: python run_kmeans.py [-h] module k max_iterations

positional arguments:
  module          data module
  k               number of clusters
  max_iterations  maximum number of iterations

optional arguments:
  -h, --help      show this help message and exit
```

## Running the ARFF-to-Python converter
As a convenient starting point, I used the [Weka] (http://www.cs.waikato.ac.nz/ml/weka/index.html "Weka") ARFF iris data and converted it to a module. 
```
usage: convert_arff.py [-h] file

Convert Weka ARFF files.

positional arguments:
  file        an ARFF file

optional arguments:
  -h, --help  show this help message and exit
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
