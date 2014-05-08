#TODO: this is implemented as a sqla adaptor but could stand on its own to
#get rid of the sqla requirement

import sqla

class SQLite(sqla.SQLAlchemy):

    def __init__(self, sqla_metadata, aggregate_mappers, db_file_path=None):
        engine_url = 'sqlite://' if db_file_path is None \
                     else 'sqlite:///%s' % db_file_path
        super(SQLite, self).__init__(
            sqla_metadata, aggregate_mappers, engine_url)
