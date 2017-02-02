import unittest
from mlearn.data.filter import Filter
import os

class ConverterTestCase(unittest.TestCase):

    def file_lines(self, filename):
        try:
            f = open(filename)
            lines = f.readlines()
        finally:
            f.close()
        return lines

    def testConvertIris(self):
        """ Test that the iris.py ARFF file is filtered as expected """

        input_lines = self.file_lines('mlearn/data/iris.py')
        expected = self.file_lines('mlearn/data/iris_numeric.py')
        fltr = Filter('mlearn.data.iris', ['class'])
        result = fltr.run() 
        out_file = 'iris_numeric.actual' 
        f = open(out_file, 'w')
        f.write(result)
        f.close()
        actual = self.file_lines(out_file)
        os.remove(out_file)
        for e, a in zip(expected, actual): 
            self.assertEqual(e, a, msg='Lines are different! Expected: %s, got %s' % (e, a))
