As a **user** I want to **query a materialized view**.

```python
>>> import query_tools
>>> import mapping_tools
>>> import test_data.zoo
>>> import sqlalchemy
>>> sqla_metadata = sqlalchemy.MetaData()
>>> goose_mv = sqlalchemy.Table(
...     'geese_mv', sqla_metadata,
...     sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
...     sqlalchemy.Column('name', sqlalchemy.Unicode, index=True),
...     sqlalchemy.Column('favorite_penguin_id', sqlalchemy.Integer,
...                       primary_key=True),
...     sqlalchemy.Column('favorite_penguin_name', sqlalchemy.Unicode,
...     		  index=True),
...     sqlalchemy.Column('favorite_penguin_mood', sqlalchemy.Unicode,
...			  index=True))
>>> penguin_properties = ('favorite_penguin_name', 'favorite_penguin_mood',
...                       'favorite_penguin_id')
>>> aggregate_goose_schema = mapping_tools.AggregateSchema(Goose, {
...     penguin_properties:mapping_tools.make_constructor(
...         Penguin, prefix='favorite_penguin_')})
>>> likes_puck = query_tools.Criteria(('favorite_penguin', 'name'), 'puck')
>>> my_session_manager = query_tools.SQLAlchemy(
...     sqla_metadata, {aggregate_goose_schema:goose_mv})
>>> with my_session_manager.make_session() as session:
...     query = session.query(test_data.zoo.Goose, likes_puck)
...     str(query)

```
