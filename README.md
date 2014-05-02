```shell
$ pip install git+ssh://git@github.com/natb1/mapping_tools.git
```
...a collection of strategies for object persistence.

## Repository and Encoder Sessions
Repository sessions implement strategies for querying:
```python
class MyRepositorySession:
    def query(ModelType, criteria):
        ...
        return model_type_objects
```
... where `ModelType` is the type of object to query, `criteria` is a 
[`query_tools.Criteria`]() object or a [`query_tools.Conjuction`]() object,
and `model_type_objects` is an iterator of `ModelType` objects.

Encoder sessions handle domain objects:
```python
class MyEncoderSession:
    def add_all(self, domain_objects):
        ...
```

Encoder and repository sessions are handled by session managers:
```python
class MySessionManager:
    def make_session(self):
        ...
        return context_manager
```
... where `context_manager` is a [python context manager]() that returns a
repository or encoder session on entry.

## Query criteria objects
[Query objects](http://martinfowler.com/eaaCatalog/queryObject.html) to be
passed to the [`query`]() method of repositories:
```python
query_tools.Criteria(path, value, operator)
```
... where `path` is a iterator that interprets the path to the criterion,
`value` is the value to be compared at that path, and `operator` interprets the 
comparison.
```python
query_tools.Conjuction(conjuction, criteria)
```
... where `conjuction` interprets the conjuction to be used and `criteria` is
an iterator of criteria.

## The SQLAlchemy session manager
```python
query_tools.SQLAlchemy(sqla_metadata, materialized_mappers=None)
```

## The JSON session manager

## The CSV session manager
