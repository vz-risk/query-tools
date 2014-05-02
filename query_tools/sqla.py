import sqlalchemy
import sqlalchemy.orm

import mapping_tools

class SQLAlchemy(object):

    def __init__(self, sqla_metadata, aggregate_mappers,
                 engine_url='sqlite://'):
        self.sqla_metadata = sqla_metadata
        self.aggregate_mappers = aggregate_mappers
        self.engine = sqlalchemy.create_engine(engine_url)
        self.session_maker = sqlalchemy.sessionmaker(bind=self.engine)

    def make_session(self):
        session = SQLAlchemySession(
            self.session_maker, aggregate_mappers)
        return session

    def setup(self):
        self.sqla_metadata.create_all(engine=self.engine)

class SQLAlchemySession(object):

    def __init__(self, session_maker, aggregate_mappers):
        self.sqla_session = session_maker()
        self.aggregate_mappers = aggregate_mappers

    def add_all(self, domain_objects):
        self.sqla_session.add_all(domain_objects)

    def query(self, ModelType, criteria):
        aggregate_schema = self._get_aggregate_schema(ModelType)
        sqla_criterion = self._get_sqla_criterion(ModelType, criteria)
        domain_objects = self._select_domain_objects(
            aggregate_schema, sqla_criterion)
        #TODO: self._merge_domain_objects(domain_objects)
        return domain_objects

    def _get_aggregate_schema(self, ModelType):
        #TODO: memoize this lookup
        for aggregate_schema in aggregate_mappers:
            if aggregate_schema.ModelType is ModelType:
                return aggregate_schema

    def _get_sqla_criterion(ModelType, criteria, aggregate_schema):
        if hasattr(criteria, 'conjuction'):
            if criteria.conjunction == 'and':
                sub_criteria = [SQLAlchemySession._get_sqla_criterion(
                                    ModelType, sub, aggregate_schema)
                                for sub in criteria)]
                return sqlalchemy.and_(*sub_criteria)
            elif criteria.conjuction == 'or':
                sub_criteria = [SQLAlchemySession._get_sqla_criterion(
                                    ModelType, sub, aggregate_schema)
                                for sub in criteria)]
                return sqlalchemy.or_(*sub_criteria)
        else: # if not a conjuction
            prop = self._get_sqla_property(aggregate_schema.ModelType, 
                                           criteria.path)
            if criteria.operator == 'in':
                return prop.in_(criteria.value)

    def _get_sqla_property(ModelType, path):
        prop_name = '_'.join(path)
        sqla_prop = getattr(ModelType, prop_name)
        return sqla_prop

    def _select_domain_objects(aggregate_schema, sqla_criterion):
        sqla_connection = self.sqla_session.connection(
            aggregate_schema.ModelType)
        select = sqlalechemy.sql.select(
            [self.aggregate_mappers[aggregate_schema]).where(sqla_criterion)
        materialized_results = sqla_connection.execute(select)
        results = [self.aggregate_schema.map(result)
                   for result in materialized_results]
        return results

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.sqla_session.commit()
        self.sqla_session.close()
