#TODO: use the elasticsearch python api

import datetime
import json
import os
import subprocess
import tempfile

import mapping_tools

import query_tools.json_encoder

class ElasticSearch(object):

    def __init__(self, index, ModelType_to_type_name, host='localhost:9200'):
        self.index = index
        self.ModelType_to_type_name = ModelType_to_type_name
        self.type_name_to_dict_mapper = dict(
            (type_name, mapping_tools.DictMapper(ModelType))
            for ModelType, type_name in ModelType_to_type_name.items())
        self.host = host

    def make_session(self):
        session = ElasticSearchSession(
            self.index, self.ModelType_to_type_name,
            self.type_name_to_dict_mapper, self.host)
        return session

    def setup(self):
        raise NotImplementedError()

class ElasticSearchSession(object):

    def __init__(self, index, ModelType_to_type_name,
                 type_name_to_dict_mapper, host):
        self.index = index
        self.ModelType_to_type_name = ModelType_to_type_name
        self.type_name_to_dict_mapper = type_name_to_dict_mapper
        self.host = host

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass #do nothing

    def add_all(self, domain_objects):
        #TODO: handle multiple types
        type_name = self.ModelType_to_type_name.values()[0]
        dict_mapper = self.type_name_to_dict_mapper[type_name]
        index_json = json.dumps({'index':{'_type':type_name}})
        bulkfile = tempfile.NamedTemporaryFile()
        MAX_FILE_SIZE = 104857600
        SAFE_FILE_SIZE = MAX_FILE_SIZE/2
        for obj in domain_objects:
            bulkfile.write(index_json)
            bulkfile.write('\n')
            dict_obj = dict_mapper.map(obj)
            bulkfile.write(json.dumps(
                dict_obj, cls=ISODateTimeNoMicrosecond))
            bulkfile.write('\n')
            if os.stat(bulkfile.name).st_size > SAFE_FILE_SIZE:
                self._flush_bulkfile(bulkfile)
                bulkfile = tempfile.NamedTemporaryFile()
        self._flush_bulkfile(bulkfile)
        
    def _flush_bulkfile(self, bulkfile):
        bulkfile.flush()
        try:
            out = subprocess.check_output(
                'curl -sS -XPOST {}/{}/_bulk --data-binary @{}'.format(
                    self.host, self.index, bulkfile.name),
                shell=True, stderr=subprocess.STDOUT)
            results = json.loads(out)
            if 'error' in results \
            or ('errors' in results and results['errors']):
                print out
        except subprocess.CalledProcessError as e:
            print(e.output)
        bulkfile.close()

    def query(self, ModelType, criteria):
        pass

class ISODateTimeNoMicrosecond(json.JSONEncoder):
    '''
    elasticsearch doesn't like the microseconds in python iso datetimes
    so convert them to milliseconds
    '''
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            microseconds = (obj.microsecond / 1000)
            no_microseconds = datetime.datetime(
                obj.year, obj.month, obj.day, obj.hour, obj.minute, obj.second)
            iso_with_milliseconds = '{0}.{1:03d}'.format(
                no_microseconds.isoformat(), microseconds)
            return iso_with_milliseconds
        else:
            return super(DateTimeJSONEncoder, self).default(obj)
