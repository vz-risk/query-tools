#TODO: this is implemented as a sqla adaptor but could stand on its own to
#get rid of the sqla requirement

import itertools

import mapping_tools

import sqla

class SQLite(sqla.SQLAlchemy):

    def __init__(self, sqla_metadata, aggregate_mappers, model_mappers,
                 db_file_path=None):
        self.model_mappers = model_mappers
        engine_url = 'sqlite://' if db_file_path is None \
                     else 'sqlite:///%s' % db_file_path
        super(SQLite, self).__init__(
            sqla_metadata, aggregate_mappers, engine_url)

    def make_session(self):
        return SQLiteSession(
            self.session_maker, self.aggregate_mappers, self.model_mappers)

class SQLiteSession(sqla.SQLAlchemySession):

    def __init__(self, session_maker, aggregate_mappers, model_mappers):
        self.model_mappers = model_mappers
        super(SQLiteSession, self).__init__(session_maker, aggregate_mappers)

    def add_all(self, domain_objects):
        self._materialize_objects(domain_objects)
        super(SQLiteSession, self).add_all(domain_objects)

    def _materialize_objects(self, domain_objects):
        #mapped_objects = self._get_mapped_objects(domain_objects)
        #TODO: this stub assumes only one mapped object type
        #TODO: also this generally a bit of a clusterfuck
        mapped_objects = [self.model_mappers.map(obj) 
                          for obj in domain_objects]
        self.sqla_session.add_all(mapped_objects)

