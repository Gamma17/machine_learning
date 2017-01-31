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
        self.data = data
        self.instances = []
        self.clusters = []

    def init_clusters(self, k):
        """ Randomly assign objects to k clusters """

        # TODO If a cluster has never had an instance, it could have no mean, just [],
        # should have zero mean. Fix!
        for i in range(k):
            self.clusters.append(Cluster(i))

        instance_id = 0
        for instance in self.data:
            ncluster = random.randint(0, k - 1)
            cinstance = ClusteredInstance(instance_id, instance, ncluster)
            self.instances.append(cinstance)
            instance_id += 1
        self.update_means(k)

    def cluster_mean(self, instances_data_list):
        return sum(instances_data_list) / len(instances_data_list)

    def update_means(self, k):
        """ Compute and update the cluster means """

        cluster_instances = []
        for i in range(k):
            cluster_instances.append([])

        for instance in self.instances:
            cluster = instance.cluster
            cluster_instances[cluster].append(instance.data)

        # TODO If a cluster has never had an instance, it could have no mean, just [],
        # should have zero mean. Fix!
        for i in range(k):
            if len(cluster_instances[i]) == 0:
                self.clusters[i].mean = [0] * k # TODO have a look at this, as zero is not right!
            else:
                self.clusters[i].mean = map(self.cluster_mean, zip(*(cluster_instances[i])))

    def closest_cluster(self, instance):
        """ Returns the closest cluster to the instance """

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

