import csv
import sys

import mapping_tools
import mapping_tools.heuristics

class CSVEncoder(object):

    def __init__(self, aggregate_mapper, fieldnames=None, csvfile=sys.stdout):
        self.aggregate_mapper = aggregate_mapper
        self.fieldnames = fieldnames
        self.aggregate_dict_mapper = mapping_tools.DictMapper(
            self.aggregate_mapper.ModelPrimeType)
        self.csvfile = csvfile

    def make_session(self):
        return CSVEncoderSession(
            self.aggregate_mapper, self.aggregate_dict_mapper,  self.csvfile,
            self.fieldnames)

class CSVEncoderSession(object):

    def __init__(self, aggregate_mapper, aggregate_dict_mapper, csvfile,
                 fieldnames):
        self.aggregate_mapper = aggregate_mapper
        self.aggregate_dict_mapper = aggregate_dict_mapper
        #TODO: this relies on an impelementation detail of the dict mapper
        #a better solution probably involves using extrasaction to
        #print "all" fields
        if fieldnames is None:
            fieldnames = mapping_tools.heuristics.properties(
                self.aggregate_mapper.ModelPrimeType)
        self.csv_writer = csv.DictWriter(
            csvfile, fieldnames, extrasaction='ignore')

    def __enter__(self):
        self.csv_writer.writeheader()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass # do nothing

    def add_all(self, model_objects):
        for obj in model_objects:
            aggregate_obj = self.aggregate_mapper.map(obj)
            dict_obj = self.aggregate_dict_mapper.map(aggregate_obj)
            self._fix_unicode(dict_obj)
            self.csv_writer.writerow(dict_obj)

    @staticmethod
    def _fix_unicode(dict_obj):
        '''
        side effect: fix encoding for all values in dict so
        they can be handled by the csv writer
        '''
        for key, value in dict_obj.items():
            if type(value) is unicode:
                dict_obj[key] = value.encode('utf8')
