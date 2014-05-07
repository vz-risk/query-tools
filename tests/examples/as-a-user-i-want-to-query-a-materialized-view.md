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
>>> aggregate_goose_schema = mapping_tools.Mapper(test_data.zoo.Goose, {
...     ('name', 'id'):mapping_tools.identity,
...     penguin_properties:mapping_tools.make_constructor(
...         test_data.zoo.Penguin, 'favorite_penguin')})
>>> my_session_manager = query_tools.SQLAlchemy(
...     sqla_metadata, {aggregate_goose_schema:goose_mv})
>>> my_session_manager.setup()
>>> likes_puck = query_tools.Criteria(('favorite_penguin', 'name'), (u'puck',))
>>> with my_session_manager.make_session() as session:
...     select = session.get_select(test_data.zoo.Goose, likes_puck)
...     print(select) # doctest: +NORMALIZE_WHITESPACE
SELECT 
    geese_mv.id, geese_mv.name, geese_mv.favorite_penguin_id, 
    geese_mv.favorite_penguin_name, geese_mv.favorite_penguin_mood 
FROM geese_mv 
WHERE geese_mv.favorite_penguin_name IN (:favorite_penguin_name_1)

```
