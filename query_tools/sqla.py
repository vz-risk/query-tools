import sqlalchemy
import sqlalchemy.orm

import mapping_tools

class SQLAlchemy(object):

    def __init__(self, sqla_metadata, aggregate_mappers,
                 engine_url='sqlite://'):
        self.sqla_metadata = sqla_metadata
        self.aggregate_mappers = aggregate_mappers
        self.engine = sqlalchemy.create_engine(engine_url)
        self.session_maker = sqlalchemy.orm.sessionmaker(bind=self.engine)

    def make_session(self):
        session = SQLAlchemySession(
            self.session_maker, self.aggregate_mappers)
        return session

    def setup(self):
        self.sqla_metadata.create_all(self.engine)

#TODO: contained clusterfuck
class SQLAlchemySession(object):

    def __init__(self, session_maker, aggregate_mappers):
        self.sqla_session = session_maker()
        self.aggregate_mappers = aggregate_mappers

    def add_all(self, domain_objects):
        self.sqla_session.add_all(domain_objects)

    def query(self, ModelType, criteria):
        aggregate_schema = self._get_aggregate_schema(ModelType)
        aggregate_table = self.aggregate_mappers[aggregate_schema]
        sqla_criterion = self._get_sqla_criterion(
            ModelType, criteria, aggregate_schema, aggregate_table)
        domain_objects = self._select_domain_objects(
            aggregate_schema, sqla_criterion)
        #TODO: self._merge_domain_objects(domain_objects)
        return domain_objects

    #TODO: this is only used for testing and involves duplicate code from
    #SQLAlchemySession.query and SQLAlchemySession._select_domain_objects
    def get_select(self, ModelType, criteria):
        aggregate_schema = self._get_aggregate_schema(ModelType)
        aggregate_table = self.aggregate_mappers[aggregate_schema]
        sqla_criterion = self._get_sqla_criterion(
            ModelType, criteria, aggregate_schema, aggregate_table)
        aggregate_table = self.aggregate_mappers[aggregate_schema]
        sqla_connection = self.sqla_session.connection()
        select = aggregate_table.select().where(sqla_criterion)
        return select

    def _get_aggregate_schema(self, ModelType):
        #TODO: memoize this lookup
        for aggregate_schema in self.aggregate_mappers:
            if aggregate_schema.ModelPrimeType is ModelType:
                return aggregate_schema

    @staticmethod
    def _get_sqla_criterion(ModelType, criteria, aggregate_schema,
                            aggregate_table):
        if hasattr(criteria, 'conjunction'):
            if criteria.conjunction == 'and':
                sub_criteria = SQLAlchemySession._get_subcriteria(
                    ModelType, aggregate_schema, criteria, aggregate_table)
                return sqlalchemy.and_(*sub_criteria)
            elif criteria.conjuction == 'or':
                sub_criteria = SQLAlchemySession._get_subcriteria(
                    ModelType, aggregate_schema, criteria, aggregate_table)
                return sqlalchemy.or_(*sub_criteria)
        else: # if not a conjuction
            prop = SQLAlchemySession._get_sqla_property(
                aggregate_table, criteria.path)
            if criteria.operator == 'in':
                return prop.in_(criteria.value)

    @staticmethod
    def _get_subcriteria(ModelType, aggregate_schema, criteria,
                         aggregate_table):
        subcriteria = [SQLAlchemySession._get_sqla_criterion(
                           ModelType, sub, aggregate_schema, aggregate_table)
                       for sub in criteria]
        return subcriteria

    @staticmethod
    def _get_sqla_property(aggregate_table, path):
        prop_name = '_'.join(path)
        sqla_prop = aggregate_table.columns[prop_name]
        return sqla_prop

    def _select_domain_objects(self, aggregate_schema, sqla_criterion):
        aggregate_table = self.aggregate_mappers[aggregate_schema]
        sqla_connection = self.sqla_session.connection()
        select = aggregate_table.select().where(sqla_criterion)
        materialized_results = sqla_connection.execute(select)
        results = [self.aggregate_schema.map(result)
                   for result in materialized_results]
        return results

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.sqla_session.commit()
        self.sqla_session.close()
