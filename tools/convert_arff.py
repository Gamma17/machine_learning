"""
This tool converts Weka ARFF files to python modules.
See http://weka.wikispaces.com/ARFF+%28book+version%29
This tool is designed to work with the arff files districuted with Weka version 3.6.14.
"""

import argparse

def convert_line(line):
    line = line.lstrip()
    if line[0] == '%':
        line = '#' + line[1:]
    elif line[0] == '@':
        # relation, attribute or data? (Case insensitive)
        pass
    return line

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert Weka ARFF files.')
    parser.add_argument('file', type=str, help='an arff file')
    args = parser.parse_args()
    try:
        with open(args.file) as f:
            lines = f.readlines()
            output = ''
            for line in lines:
                line = convert_line(line)
                output += line
            print output
    except IOError:
        print 'Problem reading file:', args.file
