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
        self.instances = [Instance(i, data[i], None) for i in range(len(data))]

    def init_clusters(self, k):
        """ Randomly assign objects to k clusters """

        # TODO If a cluster has never had an instance, it could have no mean, just [],
        # should have zero mean. Fix!
        dim = len(self.instances[0].data)
        self.clusters = [Cluster(i, dim) for i in range(k)]

        for instance in self.instances:
            ncluster = random.randint(0, k - 1)
            instance.cluster = self.clusters[ncluster]
        self.update_means(k)

    def mean(self, data):
        return sum(data) / len(data)

    def update_means(self, k):
        """ Compute and update the cluster means """

        cluster_instances = {c: [] for c in self.clusters}

        for instance in self.instances:
            cluster = instance.cluster
            cluster_instances[cluster].append(instance)

        for clust, insts in cluster_instances.iteritems():
            if len(insts) == 0:
                dim = len(self.instances[0].data)
                clust.mean = [0] * dim # TODO have a closer look at this!
            else:
                data = [instance.data for instance in insts]
                clust.mean =  map(self.mean, zip(*(data)))

    def closest_cluster(self, instance):
        """ Returns the closest cluster to the instance """

        closest_cluster = instance.cluster
        shortest_distance = sys.maxint
        for cluster in self.clusters:
            distance = Distance.euclidean(instance.data, cluster.mean)
            if distance < shortest_distance:
                shortest_distance = distance
                closest_cluster = cluster
        return closest_cluster

    def run(self, k, max_iterations):
        """
        Run k-means: load data and iterate until no changes occur
        or maximum iterations reached.
        """
        
        # Initialize clusters
        self.init_clusters(k)

        iteration = 1
        while iteration <= max_iterations:
            changed = False
            for instance in self.instances:
                closest_cluster = self.closest_cluster(instance)
                if instance.cluster != closest_cluster:
                    instance.cluster = closest_cluster
                    changed = True
            if changed:
                iteration += 1
                self.update_means(k)
            else:
                break

class Cluster(object):
    """ A cluster with centre equal to the mean of its members """

    def __init__(self, name, dim):
        self.name = name
        self.mean = [0] * dim

    def __str__(self):
        return str(self.name) + '::' + str(self.mean)

class Instance(object):
    """ Instance assigned to a cluster """

    def __init__(self, name, data, cluster):
        self.name = name
        self.data = data
        self.cluster = cluster

    def __str__(self):
        return str(self.name) + '::' + str(self.data) + '::' + str(self.cluster.name)

