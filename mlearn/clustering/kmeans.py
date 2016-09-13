import importlib

class Kmeans(object):
    """ Implements the k-means clustering algorithm """
    
    def __init__(self, data_module, k, max_iterations):
        self.mod = importlib.import_module(data_module)
        self.k = k
        self.max_iterations = max_iterations

    def run(self):
        relation = getattr(self.mod, 'relation')
        attributes = getattr(self.mod, 'attributes')
        data = getattr(self.mod, 'data')

class ClusteredInstance(object):
    """ Instance assigned to a cluster """

    def __init__(self):
        self.cluster = -1
