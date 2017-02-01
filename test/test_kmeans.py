import unittest
from mlearn.clustering import kmeans

class ConverterTestCase(unittest.TestCase):

    def test_cluster_mean(self):
        data = [[1.1, 4.2, 3.7]]
        km = kmeans.Kmeans(data)
        expected = 3.0
        actual = km.mean(data[0])
        self.assertEqual(actual, expected, msg='Expected %f, got %f' % (expected, actual))

    def test_update_means(self):
        data = [[1.1, 4.2, 3.7],
                [2.2, 7.1, 10.1],
                [3.4, 34.1, 22.5],
                [7.1, 8.2, 3.0],
                [0.2, 0.9, 1.7],
                [8.8, 11.2, 4.6]]
        k = 3

        clust00 = kmeans.Cluster(0)
        clust01 = kmeans.Cluster(1)
        clust02 = kmeans.Cluster(2)

        inst00 = kmeans.Instance(0, data[0])
        inst01 = kmeans.Instance(1, data[1])
        inst02 = kmeans.Instance(2, data[2])
        inst03 = kmeans.Instance(3, data[3])
        inst04 = kmeans.Instance(4, data[4])
        inst05 = kmeans.Instance(5, data[5])

        inst00.cluster = clust00
        inst01.cluster = clust01
        inst02.cluster = clust01
        inst03.cluster = clust02
        inst04.cluster = clust02
        inst05.cluster = clust02

        clust00.append(inst00)
        clust01.append(inst01)
        clust01.append(inst02)
        clust02.append(inst03)
        clust02.append(inst04)
        clust02.append(inst05)

        km = kmeans.Kmeans(data)
        km.instances = [inst00, inst01, inst02, inst03, inst04, inst05]
        km.clusters = [clust00, clust01, clust02]
        km.update_means(k)

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

    def test_run(self):
        data = [[1, 2, 3, 4],
                [20, 21, 22, 23],
                [24, 25, 26, 27],
                [300, 301, 302, 303],
                [303, 302, 301, 300],
                [305, 310, 315, 316]]
        k = 3

        clust00 = kmeans.Cluster(0)
        clust01 = kmeans.Cluster(1)
        clust02 = kmeans.Cluster(2)

        inst00 = kmeans.Instance(0, data[0])
        inst01 = kmeans.Instance(1, data[1])
        inst02 = kmeans.Instance(2, data[2])
        inst03 = kmeans.Instance(3, data[3])
        inst04 = kmeans.Instance(4, data[4])
        inst05 = kmeans.Instance(5, data[5])

        inst00.cluster = clust00
        inst01.cluster = clust00
        inst02.cluster = clust01
        inst03.cluster = clust01
        inst04.cluster = clust01
        inst05.cluster = clust02

        km = kmeans.Kmeans(data)
        km.instances = [inst00, inst01, inst02, inst03, inst04, inst05]
        km.clusters = [clust00, clust01, clust02]
        km.update_means(k)

        km.run(k, 100, False)

        self.assertEqual(inst01.cluster, inst02.cluster, msg="inst01 and inst02 not in the same cluster!")
        self.assertEqual(inst03.cluster, inst04.cluster, msg="inst03 and inst04 not in the same cluster!")
        self.assertEqual(inst04.cluster, inst05.cluster, msg="inst04 and inst05 not in the same cluster!")
