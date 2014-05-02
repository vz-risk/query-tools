As a **user** I want to **query a relational db**.
```python
>>> import query_tools
>>> import test_data.zoo
>>> import sqlalchemy
>>> import sqlalchemy.orm
>>> sqla_metadata = sqlalchemy.MetaData()
>>> penguin_table = sqlalchemy.Table(
...     'penguins', sqla_metadata,
...     sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
...     sqlalchemy.Column('name', sqlalchemy.Unicode, index=True),
...     sqlalchemy.Column('mood', sqlalchemy.Unicode, index=True))
>>> goose_table = sqlalchemy.Table(
...     'geese', sqla_metadata,
...     sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
...     sqlalchemy.Column('name', sqlalchemy.Unicode, index=True),
...     sqlalchemy.Column('favorite_penguin_id', sqlalchemy.Integer,
...                       ForeignKey(penguin_table.columns['id']))
>>> sqlalchemy.orm.mapper(test_data.zoo.Penguin, penguin_table)
>>> sqlalchemy.orm.mapper(test_data.zoo.Goose, goose_table, {
...     'favorite_penguin':sqlalchemy.relationship(Penguin)})
>>> likes_puck = query_tools.Criteria(('favorite_penguin', 'name'), 'puck')
>>> my_session_manager = query_tools.SQLAlchemy(sqla_metadata)
>>> with my_session_manager.make_session() as session:
...     query = session.query(test_data.zoo.Goose, likes_puck)
...     str(query)

```
