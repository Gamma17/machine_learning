import unittest
from mlearn.clustering import kmeans

class ConverterTestCase(unittest.TestCase):

    def test_cluster_mean(self):
        data = [1.1, 4.2, 3.7]
        km = kmeans.Kmeans(data)
        expected = 3.0
        actual = km.mean(data)
        self.assertEqual(actual, expected, msg='Expected %f, got %f' % (expected, actual))

    def test_update_means(self):
        data = [[1.1, 4.2, 3.7],
                [2.2, 7.1, 10.1],
                [3.4, 34.1, 22.5],
                [7.1, 8.2, 3.0],
                [0.2, 0.9, 1.7],
                [8.8, 11.2, 4.6]]
        k = 3
        dim = 3

        clust00 = kmeans.Cluster(0, dim)
        clust01 = kmeans.Cluster(1, dim)
        clust02 = kmeans.Cluster(2, dim)
        clust03 = kmeans.Cluster(3, dim)

        inst00 = kmeans.Instance(0, data[0], clust00)
        inst01 = kmeans.Instance(1, data[1], clust01)
        inst02 = kmeans.Instance(2, data[2], clust01)
        inst03 = kmeans.Instance(3, data[3], clust02)
        inst04 = kmeans.Instance(4, data[4], clust02)
        inst05 = kmeans.Instance(5, data[5], clust02)

        km = kmeans.Kmeans(data)
        km.instances = [inst00, inst01, inst02, inst03, inst04, inst05]
        km.clusters = [clust00, clust01, clust02, clust03]
        km.update_means(3)

        expected = [1.1, 4.2, 3.7]
        actual = km.clusters[0].mean
        for e, a in zip(expected, actual):
            self.assertAlmostEqual(e, a, msg='Lists not even almost equal! Expected %s, got %s' % (expected, actual))

        expected = [2.8, 20.6, 16.3]
        actual = km.clusters[1].mean
        for e, a in zip(expected, actual):
            self.assertAlmostEqual(e, a, msg='Lists not even almost equal! Expected %s, got %s' % (expected, actual))

        expected = [5.366666666666667, 6.766666666666667, 3.1]
        actual = km.clusters[2].mean
        for e, a in zip(expected, actual):
            self.assertAlmostEqual(e, a, msg='Lists not even almost equal! Expected %s, got %s' % (expected, actual))

        expected = [0, 0, 0]
        actual = km.clusters[3].mean
        self.assertEqual(expected, actual, msg='Expected %s, got %s' % (expected, actual))
