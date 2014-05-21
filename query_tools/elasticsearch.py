#TODO: use the elasticsearch python api

import json
import subprocess
import tempfile

import mapping_tools

import query_tools.json_encoder

class ElasticSearch(object):

    def __init__(self, index, ModelType_to_type_name):
        self.index = index
        self.ModelType_to_type_name = ModelType_to_type_name
        self.type_name_to_dict_mapper = dict(
            (type_name, mapping_tools.DictMapper(ModelType))
            for ModelType, type_name in ModelType_to_type_name.items())

    def make_session(self):
        session = ElasticSearchSession(
            self.index, self.ModelType_to_type_name,
            self.type_name_to_dict_mapper)
        return session

    def setup(self):
        raise NotImplementedError()

class ElasticSearchSession(object):

    def __init__(self, index, ModelType_to_type_name,
                 type_name_to_dict_mapper):
        self.index = index
        self.ModelType_to_type_name = ModelType_to_type_name
        self.type_name_to_dict_mapper = type_name_to_dict_mapper

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass #do nothing

    def add_all(self, domain_objects):
        #TODO: handle multiple types
        type_name = self.ModelType_to_type_name[domain_objects[0].__class__]
        dict_mapper = self.type_name_to_dict_mapper[type_name]
        model_dict_objects = [dict_mapper.map(obj) for obj in domain_objects]
        index_json = json.dumps({'index':{'_type':type_name}})
        bulkfile = tempfile.NamedTemporaryFile()
        for obj in model_dict_objects:
            bulkfile.write(index_json)
            bulkfile.write('\n')
            bulkfile.write(json.dumps(
                obj, cls=query_tools.json_encoder.DateTimeJSONEncoder))
            bulkfile.write('\n')
        bulkfile.flush()
        subprocess.call('curl -s -XPOST localhost:9200/{}/_bulk --data-binary @{}'.format(self.index, bulkfile.name), shell=True)
        bulkfile.close()

    def query(self, ModelType, criteria):
        pass
