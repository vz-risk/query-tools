import sqlalchemy
import sqlalchemy.orm

import fixture_model

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
sqlalchemy.orm.mapper(fixture_model.Penguin, penguin_table)
sqlalchemy.orm.mapper(fixture_model.Goose, goose_table, {
    'favorite_penguin':sqlalchemy.orm.relationship(fixture_model.Penguin)})
