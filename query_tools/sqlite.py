#TODO: this is implemented as a sqla adaptor but could stand on its own to
#get rid of the sqla requirement

import itertools

import mapping_tools

import sqla

class SQLite(sqla.SQLAlchemy):
    # TODO: unittest to discover issue with creating multiple sessions
    # or the same db

    # sqlite doesn't play well with concurrency so they all work on the same
    # connection and only close it when no longer in use
    shared_sessions = [] 

    def __init__(self, sqla_metadata, aggregate_mappers, model_mappers,
                 db_file_path=None):
        self.model_mappers = model_mappers
        engine_url = 'sqlite://' if db_file_path is None \
                     else 'sqlite:///%s' % db_file_path
        super(SQLite, self).__init__(
            sqla_metadata, aggregate_mappers, engine_url)

    def make_session(self):
        session = SQLiteSession(self.shared_sessions, self.session_maker,
                                self.aggregate_mappers, self.model_mappers)
        self.shared_sessions.append(session)
        return session

class SQLiteSession(sqla.SQLAlchemySession):

    def __init__(self, shared_sessions, session_maker, aggregate_mappers,
                 model_mappers):
        self.shared_sessions = shared_sessions
        self.model_mappers = model_mappers
        if len(self.shared_sessions) > 0:
            self.sqla_session = self.shared_sessions[0].sqla_session
            self.aggregate_mappers = aggregate_mappers
        else:
            super(SQLiteSession, self).__init__(
                session_maker, aggregate_mappers)

    def __exit__(self, exc_type, exc_value, traceback):
        self.sqla_session.commit()
        self.shared_sessions.remove(self)
        if len(self.shared_sessions) == 0:
            self.sqla_session.close()

    def add_all(self, domain_objects):
        super(SQLiteSession, self).add_all(domain_objects)
        self.sqla_session.commit() # to get object ids
        self._materialize_objects(domain_objects)

    def _materialize_objects(self, domain_objects):
        #mapped_objects = self._get_mapped_objects(domain_objects)
        #TODO: this stub assumes only one mapped object type
        #TODO: also this generally a bit of a clusterfuck
        mapped_objects = [self.model_mappers.map(obj) 
                          for obj in domain_objects]
        self.sqla_session.add_all(mapped_objects)

