import sqlalchemy
import sqlalchemy.orm

import query_tools
import model_fixt

sqla_metadata = sqlalchemy.MetaData()
penguin_table = sqlalchemy.Table(
    'penguins', sqla_metadata,
    sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column('name', sqlalchemy.Unicode, index=True),
    sqlalchemy.Column('mood', sqlalchemy.Unicode, index=True))
goose_table = sqlalchemy.Table(
    'geese', sqla_metadata,
    sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column('name', sqlalchemy.Unicode, index=True),
    sqlalchemy.Column('favorite_penguin_id', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey(penguin_table.columns['id'])))
sqlalchemy.orm.mapper(model_fixt.Penguin, penguin_table)
sqlalchemy.orm.mapper(model_fixt.Goose, goose_table, {
    'favorite_penguin':sqlalchemy.orm.relationship(model_fixt.Penguin)})

import data_fixt

def setup_test(test):
    sqla_session_manager = query_tools.SQLAlchemy(sqla_metadata)
    sqla_session_manager.setup()
    with sqla_session_manager.make_session() as session:
        session.add_all(data_fixt.geese)
    test.globs['my_session_manager'] = sqla_session_manager
