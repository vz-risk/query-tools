#TODO: use the elasticsearch python api

import collections
import datetime
import json
import logging
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
        #results = elasticsearch.helpers.streaming_bulk(
        #   self.es, self._get_actions(domain_objects))
        #for result in results:
        #    print(json.dumps(result, indent=2))
        results = elasticsearch.helpers.bulk(
           self.es, self._get_actions(domain_objects))

    def _get_actions(self, domain_objects):
        #TODO: domain_objects should be indexed by type to prevent
        #mapping lookups for each oject
        for obj in domain_objects:
            type_name = self.ModelType_to_type_name[type(obj)]
            dict_mapper = self.type_name_to_dict_mapper[type_name]
            action = dict_mapper.map(obj)
            #TODO: fix for todo in iocdb es session manager
            if 'id' in action and action['id'] is None:
                del action['id']
            action['_index'] = self.index
            action['_type'] = type_name
            yield action
        
    def query(self, ModelType, criteria, page_size=50000):
        schema = self.ModelType_to_schema_mapper[ModelType]
        type_name = self.ModelType_to_type_name[ModelType]
        query = {
                    'query': self._make_query(criteria),
                    'size':page_size, 'from':0
                }
        more_pages = True
        while more_pages:
            res = self.es.search(
                index=self.index, doc_type=type_name, body=query)
            query['from'] += page_size
            more_pages = query['from'] < res['hits']['total']
            model_objects = [schema.map(hit['_source']) 
                             for hit in res['hits']['hits']]
            for obj in model_objects:
                yield obj

    @staticmethod
    def _make_query(criteria, query={}):
        if hasattr(criteria, 'conjunction'):
            if criteria.conjunction == 'and':
                for subcriteria in criteria:
                    subquery = ElasticSearchSession._make_query(subcriteria)
                    query = ElasticSearchSession._update_query(query, subquery)
            elif criteria.conjunction == 'or':
                raise NotImplementedError()
        else:
            path_string = '.'.join(criteria.path)
            if criteria.operator == 'in':
                section = ElasticSearchSession._get_bool_section('must', query)
                section.append({'terms':{path_string:criteria.value}})
            elif criteria.operator == 'not in':
                section = ElasticSearchSession._get_bool_section('must_not', query)
                section.append({'terms':{path_string:criteria.value}})
            elif criteria.operator == '>=':
                section = ElasticSearchSession._get_bool_section('must', query)
                section.append({'range':{path_string:{'gte': criteria.value}}})
            elif criteria.operator == '<':
                section = ElasticSearchSession._get_bool_section('must', query)
                section.append({'range':{path_string:{'lt': criteria.value}}})
        return query

    @staticmethod
    def _update_query(query, update):
        for k, v in update.iteritems():
            if isinstance(v, collections.Mapping):
                r = ElasticSearchSession._update_query(query.get(k, {}), v)
                query[k] = r
            else:
                query[k] = update[k]
        return query

    @staticmethod
    def _get_bool_section(section, query):
        filtered = query.setdefault('filtered', {})
        filter_ = filtered.setdefault('filter', {})
        bool_ = filter_.setdefault('bool', {})
        section = bool_.setdefault(section, [])
        return section

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
