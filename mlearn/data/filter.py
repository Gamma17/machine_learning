import importlib
import pprint

class Filter(object):

    def __init__(self, data_module, attributes):
        self.data_module = data_module
        self.exclude = attributes

    def run(self):

        # Load data
        mod = importlib.import_module(self.data_module)
        relation  = getattr(mod, 'relation')
        attributes = getattr(mod, 'attributes')
        values = getattr(mod, 'values')
        data = getattr(mod, 'data')

        # Remove excluded attributes
        indices = []
        for attribute in self.exclude:
            index  = attributes.index(attribute)
            indices.append(index)
        for index in sorted(indices, reverse=True):
            del attributes[index]
            del values[index]
            for row in data:
                del row[index]

        result = "relation = '" + relation + "'\n"
        result += 'attributes  = ' + str(attributes) + '\n'
        result += 'values  = ' + str(values) + '\n'
        result += 'data  = ' + str(pprint.pformat(data)) + '\n'
        return result
