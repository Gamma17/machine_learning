#!/usr/bin/env python

"""
This tool converts Weka ARFF files to python modules.
See http://weka.wikispaces.com/ARFF+%28book+version%29
This tool is designed to work with the ARFF files distributed with Weka version 3.6.14.
It supports only numeric and nominal attributes; string, date and relation-valued attributes are not supported.
"""

import argparse
import re

class UnexpectedTokenException(Exception):
    pass

class UnsupportedAttributeException(Exception):
    pass

class ArffParser(object):

    RELATION, ATTRIBUTE, DATA = range(3)
    PATTERN = '\{(.*)\}' # for matching attribute values

    def __init__(self):
        self.expecting = ArffParser.RELATION
        self.output = ''
        self.attributes = []
        self.values = []

    def handle_comment(self, line):
        line = '#' + line[1:]
        self.output += line

    def handle_relation(self, line):
        tokens = line.split()
        if tokens[0].lower() != '@relation':
            raise UnexpectedTokenException(tokens[0] + ', in line: ' + line)
        relation = tokens[1]
        line = 'relation = ' + relation + '\n'
        self.output += line
        self.expecting = ArffParser.ATTRIBUTE

    def handle_attribute(self, line):
        tokens = line.split()
        if tokens[0].lower() != '@attribute':
            if tokens[0].lower() == '@data':
                self.output += 'attributes = ' + str(self.attributes) + '\n'
                self.output += 'values = ' + str(self.values) + '\n'
                self.expecting = ArffParser.DATA 
                return
            else:
                raise UnexpectedTokenException(tokens[0] + ', in line: ' + line)
        name = tokens[1]
        self.attributes.append(name)
        value = tokens[2]
        if value in ('numeric', 'REAL'):
            self.values.append([])
        elif value.startswith('{'):
            value_list = []
            values = re.findall(ArffParser.PATTERN, line)[0].split(',') 
            for i in range(len(values)):
                value = values[i].strip()
                value_list.append(value)
            self.values.append(value_list)
        else:
            raise UnexpectedTokenException(tokens[0] + ', in line: ' + line)

    def add_quotes(self, token):
        """ If token's not already surrounded by quotation marks, add them. """
        if not ((token[0] == "'" and token[-1] == "'") or 
                (token[0] == '"' and token[-1] == '"')):
            token = "'" + token + "'"
        return token

    def convert_line(self, line):
        line = line.lstrip()
        if line == '':
            return
        if line[0] == '%':
            line = self.handle_comment(line)
        elif self.expecting == ArffParser.RELATION:
            line = self.handle_relation(line)
        elif self.expecting == ArffParser.ATTRIBUTE:
            line = self.handle_attribute(line)
        elif self.expecting == ArffParser.DATA:
            pass

    def process(self, lines):
        output = ''
        for line in lines:
            line = self.convert_line(line)
        return self.output

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
