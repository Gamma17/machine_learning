# Simple _k_-means
An implementation of the simple _k_-means clustering algorithm in Python. 

Since Python is a dynamic language, I decided to represent the data directly in a Python module. An example is the module mlearn.data.iris_numeric. 

As a convenient starting point, I used the [Weka] (http://www.cs.waikato.ac.nz/ml/weka/index.html "Weka") ARFF iris data and converted it to a module. 

## Running _k_-means
```
python run_kmeans.py [-h] module k max_iterations

positional arguments:
  module          data module
  k               number of clusters
  max_iterations  maximum number of iterations

optional arguments:
  -h, --help      show this help message and exit
```

## Running the ARFF-to-Python converter
```
usage: convert_arff.py [-h] file

Convert Weka ARFF files.

positional arguments:
  file        an ARFF file

optional arguments:
  -h, --help  show this help message and exit
  ```
