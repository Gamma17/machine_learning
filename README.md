# Simple k-means clustering
An implementation of simple k-means. Since Python is a dynamic language, I decided to represent the data directly in a Python module. An example is the module mlearn.data.iris_numeric. As a starting point, I used the [Weka] (http://www.cs.waikato.ac.nz/ml/weka/index.html "Weka") ARFF iris data and converted it to a module.

## Running k-means
```
python run_kmeans.py [-h] module k max_iterations

positional arguments:
  module          data module
  k               number of clusters
  max_iterations  maximum number of iterations

optional arguments:
  -h, --help      show this help message and exit
```
