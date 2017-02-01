import re
import pprint


class UnexpectedTokenException(Exception):
    """ Unexpected token encountered """


class UnsupportedAttributeException(Exception):
    """ Unsupported attribute encountered: neither numeric nor nominal """


class AttributeValueException(Exception):
    """ While reading data, a value with the wrong type was encountered """


class ArffParser(object):
    """ Parses ARFF files, performs data validation, writes python output """

    PREAMBLE, RELATION, ATTRIBUTE, DATA, DATA_WRITTEN = range(5)
    PATTERN = r'\{(.*)\}'  # for matching attribute values

    def __init__(self):
        #self.expecting = ArffParser.RELATION
        self.expecting = ArffParser.PREAMBLE
        self.output = ''
        self.attributes = []
        self.values = []
        self.data = []
        self.docstring = '"""\n'

    def handle_comment(self, line):
        """ Include comments in docstring """

        if line[0] == '%':
            self.docstring += line[1:]
        else:
            self.output += self.docstring
            self.output += '"""\n'
            self.expecting = ArffParser.RELATION
            self.handle_relation(line)

    def handle_relation(self, line):
        """ Declare relation name """

        tokens = line.split()
        if tokens[0].lower() != '@relation':
            raise UnexpectedTokenException(tokens[0] + ', in line: ' + line)
        relation = tokens[1]
        if not ((relation[0] == "'" and relation[-1] == "'") or
                (relation[0] == '"' and relation[-1] == '"')):
            relation = "'" + relation + "'"
        line = 'relation = ' + relation + '\n'
        self.output += line
        self.expecting = ArffParser.ATTRIBUTE

    def handle_attribute(self, line):
        """ Add attribute names and values to lists """

        tokens = line.split()
        if tokens[0].lower() != '@attribute':
            if tokens[0].lower() == '@data':
                self.output += 'attributes = ' + str(self.attributes) + '\n'
                self.output += 'values = ' + str(self.values) + '\n'
                self.expecting = ArffParser.DATA
                return
            else:
                raise UnexpectedTokenException(
                        tokens[0] + ', in line: ' + line)
        name = tokens[1]
        self.attributes.append(name)
        value = tokens[2]
        if value in ('numeric', 'REAL'):
            self.values.append([])  # empty list means it's a float!
        elif value.startswith('{'):
            value_list = []
            values = re.findall(ArffParser.PATTERN, line)[0].split(',')
            for value in values:
                value = value.strip()
                value_list.append(value)
            self.values.append(value_list)
        else:
            raise UnexpectedTokenException(
                    tokens[0] + ', in line: ' + line)

    def handle_data(self, line):
        """ Validate data row and add to list """

        row = []
        values = line.split(',')
        if len(values) == len(self.attributes):
            for value, attribute in zip(values, self.values):
                value = value.strip()
                if attribute == []:
                    try:
                        row.append(float(value))
                    except:
                        raise AttributeValueException(
                                'Expected numeric value on line: ', + line)
                else:
                    row.append(value)
            self.data.append(row)
        else:
            if line[0] != '%':
                raise AttributeValueException(
                        'Wrong number on values on line: ' + line)

    def output_data(self):
        """ Write the data rows into the output """

        if self.expecting == ArffParser.DATA:
            self.output += 'data = ' + pprint.pformat(self.data) + '\n'
            self.expecting = ArffParser.DATA_WRITTEN

    def convert_line(self, line):
        """ Convert a line of ARFF into a Python representation """

        line = line.lstrip()
        if line == '':
            self.output_data()
            return
        if self.expecting == ArffParser.PREAMBLE:
            self.handle_comment(line)
        elif self.expecting == ArffParser.RELATION:
            self.handle_relation(line)
        elif self.expecting == ArffParser.ATTRIBUTE:
            self.handle_attribute(line)
        elif self.expecting == ArffParser.DATA:
            self.handle_data(line)

    def process(self, lines):
        """ Process lines in ARFF file one at a time """

        for line in lines:
            line = self.convert_line(line)
        self.output_data()
        return self.output

