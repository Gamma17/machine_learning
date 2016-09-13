import importlib
import random


class Distance(object):
    """ Measure distance between objects (instance, clusters) """

    @classmethod
    def euclidean(x, y):
        """ Euclidean distance between x and y """
        pass

    @classmethod
    def sq_euclidean(x, y):
        """ SquaredEuclidean distance between x and y """
        pass

class Kmeans(object):
    """ Implements the k-means clustering algorithm """
    
    def __init__(self, data_module, k, max_iterations):
        self.data_module = data_module
        self.k = k
        self.max_iterations = max_iterations
        self.values = []
        self.instances = []
        self.clusters = []
        self.nattributes = 0

    def init_clusters(self, data):
        """ Randomly assign objects to k clusters """

        for i in range(self.k):
            self.clusters.append(Cluster(i))

        instance_id = 0
        for instance in data:
            ncluster = random.randint(0, self.k - 1)
            cinstance = ClusteredInstance(instance_id, instance, ncluster)
            self.instances.append(cinstance)
            instance_id += 1
        self.update_means()

    def update_means(self):
        """ Compute and update the cluster means """
        for cluster in self.clusters:
            cluster.mean = [0] * self.nattributes 
        for instance in self.instances:
            cluster = instance.cluster
            index = 0

            # ignore nominal attributes during update
            for att, val in zip(self.values, instance.data):
                if att == []:
                    print 'updating value...', val
                    self.clusters[cluster].mean[index] += val
                    index += 1

    def run(self):
        """
        Run k-means: load data and iterate until no changes occur
        or maximum iterations reached.
        """
        
        # Load data
        mod = importlib.import_module(self.data_module)
        relation = getattr(mod, 'relation')
        self.values = getattr(mod, 'values')
        data = getattr(mod, 'data')

        # Count number of numeric attributes, ignore nominal attributes.
        for attribute in self.values:
            if attribute == []:
                self.nattributes += 1

        # Initialize clusters
        self.init_clusters(data)

        iteration = 1
        while iteration <= self.max_iterations:
            changed = False
            # if no changes occurred, finish iterations

            iteration += 1

        print 'CLUSTERS:'
        for cluster in self.clusters:
            print cluster
        print 'INSTANCES:'
        for instance in self.instances:
            print instance

class Cluster(object):
    """ A cluster with centre equal to the mean of its members """

    def __init__(self, name):
        self.name = name
        self.mean = []

    def __str__(self):
        return str(self.name) + '::' + str(self.mean)

class ClusteredInstance(object):
    """ Instance assigned to a cluster """

    def __init__(self, name, data, cluster):
        self.name = name
        self.data = data  # may include nominal data!
        self.cluster = cluster

    def __str__(self):
        return str(self.name) + '::' + str(self.data) + '::' + str(self.cluster)

