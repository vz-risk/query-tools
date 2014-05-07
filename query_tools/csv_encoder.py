import csv
import sys

import mapping_tools
import mapping_tools.heuristics

class CSVEncoder(object):

    def __init__(self, aggregate_mapper, csvfile=sys.stdout):
        self.aggregate_mapper = aggregate_mapper
        self.aggregate_dict_mapper = mapping_tools.DictMapper(
            self.aggregate_mapper.ModelPrimeType)
        self.csvfile = csvfile

    def make_session(self):
        return CSVEncoderSession(
            self.aggregate_mapper, self.aggregate_dict_mapper,  self.csvfile)

class CSVEncoderSession(object):

    def __init__(self, aggregate_mapper, aggregate_dict_mapper, csvfile):
        self.aggregate_mapper = aggregate_mapper
        self.aggregate_dict_mapper = aggregate_dict_mapper
        #TODO: this seems to rely on an impelementation detail of the dict
        #mapper
        fieldnames = mapping_tools.heuristics.properties(
            self.aggregate_mapper.ModelPrimeType)
        self.csv_writer = csv.DictWriter(csvfile, fieldnames)

    def __enter__(self):
        self.csv_writer.writeheader()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass # do nothing

    def add_all(self, model_objects):
        aggregate_objects = [self.aggregate_mapper.map(obj)
                             for obj in model_objects]
        dict_objects = [self.aggregate_dict_mapper.map(obj)
                        for obj in aggregate_objects]
        self.csv_writer.writerows(dict_objects)
