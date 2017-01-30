#!/usr/bin/env python

"""
This tool converts Weka ARFF files to python modules.

See http://weka.wikispaces.com/ARFF+%28book+version%29

Designed to work with the ARFF files distributed with Weka version 3.6.14.
Supports only numeric and nominal attributes; string, date and relation-valued
attributes are not supported.
It doesn't support missing values, represented in ARFF files by '?'.
"""

import argparse
from mlearn.data.arff_parser import ArffParser

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert Weka ARFF files.')
    parser.add_argument('file', type=str, help='an ARFF file')
    args = parser.parse_args()
    lines = None
    try:
        with open(args.file) as f:
            lines = f.readlines()
    except IOError:
        print 'Problem reading file:', args.file
    p = ArffParser()
    print p.process(lines)
