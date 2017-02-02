import unittest
from mlearn.data import arff_parser
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
        """ Test that the iris ARFF file is converted as expected """

        input_lines = self.file_lines('arff/iris.arff')
        expected = self.file_lines('mlearn/data/iris.py')
        p = arff_parser.ArffParser()
        result = p.process(input_lines)
        out_file = 'iris.actual' 
        f = open(out_file, 'w')
        f.write(result)
        f.close()
        actual = self.file_lines(out_file)
        os.remove(out_file)
        for e, a in zip(expected, actual): 
            self.assertEqual(e, a, msg='Lines are different! Expected: %s, got %s' % (e, a))
