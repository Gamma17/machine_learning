import importlib
import random
import sys
import math

class Distance(object):
    """ Measure distance between objects (instance, clusters) """

    @classmethod
    def euclidean(self, x, y):
        """ Euclidean distance between x and y """
        
        return math.sqrt(self.sq_euclidean(x, y))

    @classmethod
    def sq_euclidean(self, x, y):
        """ SquaredEuclidean distance between x and y """

        return sum([(yn - xn) ** 2 for xn, yn in zip(x, y)])

class Kmeans(object):
    """ Implements the k-means clustering algorithm """
    
    def __init__(self, data_module, k, max_iterations):
        self.data_module = data_module
        self.k = k
        self.max_iterations = max_iterations
        self.instances = []
        self.clusters = []


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
       
        # number of attributes in each instance
        nvalues  = len(self.instances[0].data)

        # init cluster means to 0 for all attributes
        means = [[0] * nvalues for c in self.clusters]

        # for tracking counts of instances in each cluster
        counts = [0] * len(self.clusters)

        for instance in self.instances:
            cluster = instance.cluster
            counts[cluster] += 1

            # update means of each cluster
            means[cluster] = [x + y for x, y in zip(means[cluster], instance.data)]

        for i in range(len(self.clusters)):
            # divide the means of each cluster through by the number of instances in the cluster
            # if there are no instances in a cluster, then division by zero could occur, so we check for this
            if counts[i] > 0:
                self.clusters[i].mean = [x / y for x, y in zip(means[i], [counts[i]] * nvalues)]

    def closest_cluster(self, instance):
        """ Returns the closest cluster to an instance """
        closest_cluster = instance.cluster
        shortest_distance = sys.maxint
        index = 0
        for cluster in self.clusters:
            distance = Distance.euclidean(instance.data, cluster.mean)
            if distance < shortest_distance:
                shortest_distance = distance
                closest_cluster = index
            index += 1
        return closest_cluster

    def run(self):
        """
        Run k-means: load data and iterate until no changes occur
        or maximum iterations reached.
        """
        
        # Load data
        mod = importlib.import_module(self.data_module)
        data = getattr(mod, 'data')

        # Initialize clusters
        self.init_clusters(data)

        iteration = 1
        while iteration <= self.max_iterations:
            changed = False
            for instance in self.instances:
                closest_cluster = self.closest_cluster(instance)
                if instance.cluster != closest_cluster:
                    instance.cluster = closest_cluster
                    changed = True
            if changed:
                iteration += 1
                self.update_means()
            else:
                break

        print 'Stopped after', iteration, 'iterations'
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
        self.data = data
        self.cluster = cluster

    def __str__(self):
        return str(self.name) + '::' + str(self.data) + '::' + str(self.cluster)

