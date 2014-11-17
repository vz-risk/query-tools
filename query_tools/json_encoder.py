import datetime
import json

import mapping_tools

class JSONEncoder(object):
    
    def __init__(self, ModelType):
        self.model_dict_mapper = mapping_tools.DictMapper(ModelType)

    def make_session(self):
        return JSONSession(self.model_dict_mapper)

class JSONSession(object):

    def __init__(self, model_dict_mapper):
        self.model_dict_mapper = model_dict_mapper

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass # do nothing

    def add(self, model_object):
        model_dict_object = self.model_dict_mapper.map(model_object)
        json_data = json.dumps(model_dict_object, indent=2, sort_keys=True,
                              cls=DateTimeJSONEncoder)
        return json_data

    #TODO: DRY JSONSession.add
    def add_all(self, model_objects):
        model_dict_objects = [self.model_dict_mapper.map(obj)
                              for obj in model_objects]
        json_data = json.dumps(model_dict_objects, indent=2, sort_keys=True,
                               cls=DateTimeJSONEncoder)
        return json_data

class DateTimeJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        else:
            return super(DateTimeJSONEncoder, self).default(obj)
