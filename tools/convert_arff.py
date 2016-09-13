#!/usr/bin/env python

"""
This tool converts Weka ARFF files to python modules.
See http://weka.wikispaces.com/ARFF+%28book+version%29
This tool is designed to work with the arff files distributed with Weka version 3.6.14.
"""

import argparse

class UnexpectedTokenException(Exception):
    pass

class ArffParser(object):

    RELATION, ATTRIBUTE, DATA, DATA_ROW = range(4)

    def __init__(self):
        self.expecting = ArffParser.RELATION

    def comment(self, line):
        line = '#' + line[1:]
        return line

    def relation(self, line):
        tokens = line.split()
        if tokens[0].lower() != '@relation':
            raise UnexpectedTokenException(tokens[0] + ', in line: ' + line)
        relation = tokens[1]

        # If it's not already surrounded in quotation marks, add them.
        if not ((relation[0] == "'" and relation[-1] == "'") or 
                (relation[0] == '"' and relation[-1] == '"')):
            relation = "'" + relation + "'"

        line = 'relation = ' + relation + '\n'
        self.expecting = ArffParser.ATTRIBUTE
        return line

    def attribute(self, line):
        return line

    def convert_line(self, line):
        line = line.lstrip()
        if line == '':
            return
        if line[0] == '%':
            line = self.comment(line)
        elif self.expecting == ArffParser.RELATION:
            line = self.relation(line)
            # relation, attribute or data? (Case insensitive)
        elif self.expecting == ArffParser.ATTRIBUTE:
            line = self.attribute(line)
            pass
        else:
            pass
        return line

    def process(self, lines):
        output = ''
        for line in lines:
            line = self.convert_line(line)
            if line:
                output += line
        return output

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
