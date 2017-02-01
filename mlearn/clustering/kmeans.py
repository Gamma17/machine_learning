from __future__ import division
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
    
    def __init__(self, data):
        self.instances = [Instance(i, data[i]) for i in range(len(data))]

    def dim(self):
        """
        Returns the dimension of an instance.
        Assumes all instances have the same dimension.
        """

        return len(self.instances[0])

    def init_clusters(self, k):
        """ Randomly assign objects to k clusters """

        self.clusters = [Cluster(i) for i in range(k)]
        for cluster in self.clusters:
            cluster.mean = [0] * self.dim()

        for instance in self.instances:
            cluster = random.choice(self.clusters) 
            instance.cluster = cluster
            cluster.append(instance)
        self.update_means(k)

    def mean(self, data):
        """ Returns the mean of a list of values """

        return sum(data) / len(data)

    def update_means(self, k):
        """ Compute and update the cluster means """

        for cluster in self.clusters:
            if len(cluster) == 0:
                cluster.mean = [0] * self.dim()
            else:
                cluster.mean =  map(self.mean, zip(*(cluster)))

    def closest_cluster(self, instance):
        """ Returns the closest cluster to the instance """

        closest_cluster = instance.cluster
        shortest_distance = sys.maxint
        for cluster in self.clusters:
            distance = Distance.euclidean(instance, cluster.mean)
            if distance < shortest_distance:
                shortest_distance = distance
                closest_cluster = cluster
        return closest_cluster

    def run(self, k, max_iterations, init=True):
        """
        Find k clusters by iterating until no changes occur or maximum iterations reached.
        You usually want init to be True, unless you're testing this method,
        in which case you will want to assign the objects to clusters in a predetermined order.
        """

        if init: 
            self.init_clusters(k)

        iteration = 1
        while iteration <= max_iterations:
            changed = False
            for instance in self.instances:
                closest_cluster = self.closest_cluster(instance)
                if instance.cluster != closest_cluster:
                    instance.cluster.remove(instance)
                    closest_cluster.append(instance) 
                    instance.cluster = closest_cluster
                    changed = True
            if changed:
                iteration += 1
                self.update_means(k)
            else:
                break

class Cluster(list):
    """ A cluster with centre equal to the mean of its members """

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return str(self.name) + '::' + str(self.mean)

class Instance(list):
    """ Instance assigned to a cluster """

    def __init__(self, name, data):
        super(Instance, self).__init__(data)
        self.name = name

    def __str__(self):
        return str(self.name) + '::' + super(Instance, self).__str__() + '::' + str(self.cluster.name)

