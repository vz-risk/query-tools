#TODO: use the elasticsearch python api

import datetime
import json
import os
import subprocess
import tempfile

import elasticsearch
import elasticsearch.helpers
import mapping_tools

import query_tools.json_encoder

class ElasticSearch(object):

    def __init__(self, index, ModelType_to_type_name,
                 ModelType_to_schema_mapper, hosts=[{'host':'localhost'}]):
        self.index = index
        self.ModelType_to_type_name = ModelType_to_type_name
        self.ModelType_to_schema_mapper = ModelType_to_schema_mapper
        self.type_name_to_dict_mapper = dict(
            (type_name, mapping_tools.DictMapper(ModelType))
            for ModelType, type_name in ModelType_to_type_name.items())
        self.hosts = hosts

    def make_session(self):
        session = ElasticSearchSession(
            self.index, self.ModelType_to_type_name,
            self.type_name_to_dict_mapper, 
            self.ModelType_to_schema_mapper,
            self.hosts)
        return session

    def setup(self):
        raise NotImplementedError()

class ElasticSearchSession(object):

    def __init__(self, index, ModelType_to_type_name,
                 type_name_to_dict_mapper,
                 ModelType_to_schema_mapper,
                 hosts):
        self.index = index
        self.ModelType_to_type_name = ModelType_to_type_name
        self.type_name_to_dict_mapper = type_name_to_dict_mapper
        self.ModelType_to_schema_mapper = ModelType_to_schema_mapper
        self.es = elasticsearch.Elasticsearch(hosts)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass #do nothing

    def add_all(self, domain_objects):
        results = elasticsearch.helpers.bulk(
           self.es, self._get_actions(domain_objects))
        print(json.dumps(results, indent=2))

    def _get_actions(self, domain_objects):
        #TODO: domain_objects should be indexed by type to prevent
        #mapping lookups for each oject
        for obj in domain_objects:
            type_name = self.ModelType_to_type_name[type(obj)]
            dict_mapper = self.type_name_to_dict_mapper[type_name]
            action = dict_mapper.map(obj)
            action['_index'] = self.index
            action['_type'] = type_name
            yield action
        
    def query(self, ModelType, criteria):
        res = self.es.search(index="iocdb", body={"query": {"match_all": {}}})
        schema = self.ModelType_to_schema_mapper[ModelType]
        objs = []
        for hit in res['hits']['hits']:
            source = hit['_source']
            obj = schema.map(source)
            objs.append(obj)
        return objs
        #return [schema.map(hit['_source']) for hit in res['hits']['hits']]

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
