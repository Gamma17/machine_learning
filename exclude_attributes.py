#!/usr/bin/env python

import argparse
import os
import mlearn.data.filter

if __name__ == '__main__':
    """
    Example: patrick@Beatrice:~/projects/machine_learning$
             python exclude_attributes.py mlearn.data.iris iris_numeric class
    """

    parser = argparse.ArgumentParser(description='Output a new module that\
            excludes specific attributes in the original module.')
    parser.add_argument('input_module', type=str, help='input data module')
    parser.add_argument('output_module_name', type=str, help='output data module name')
    parser.add_argument('attributes', type=str, nargs='+', help='input data module file')
    args = parser.parse_args()
    fltr  = mlearn.data.filter.Filter(args.input_module, args.attributes)
    output = fltr.run()

    path_tokens = args.input_module.split('.')[:-1]
    path_tokens.append(args.output_module_name + '.py')
    path = os.path.join(*path_tokens)
    
    try:
        with open(path, 'w+') as f:
            f.write(output)
            f.close()
    except IOError:
        print 'Problem opening file:', path

