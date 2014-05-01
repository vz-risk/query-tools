```shell
$ pip install git+ssh://git@github.com/natb1/mapping_tools.git
```
...a collection of strategies for object persistence.

```python
>>> import query_tools
>>> import mapping_tools
>>> import sqlalchemy
>>> goose_json_schema = mapping_tools.json_schema_mapper(goose_dict_schema)
>>> sql_metadata = sqlalchemy.MetaData()
>>> penguin_table = mapping_tools.table_mapper.map(Penguin, table_metadata)
>>> goose_table = mapping_tools.table_mapper.map(
...     Goose, table_metadata, {'favorite_penguin':Penguin})
>>> goose_aggregate_table = mapping_tools.table_mapper.map(GooseAggregate)
>>> goose_materializer = query_tools.sql_materializer.SQLMaterializer(sql_metadata)
>>> goose_materializer.setup()
>>> with goose_materializer.make_session()) as session:
...     session.add_all([grace, ginger, gail])
```
## Repository and Encoder Sessions
Repository sessions implement strategies for querying:
```python
class MyRepositorySession:
    def query(criteria):
        ...
        return domain_objects
```
