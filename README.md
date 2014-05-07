```shell
$ pip install git+ssh://git@github.com/natb1/query_tools.git
```
...a collection of strategies for object persistence. For example, these 
objects:
>>> class Penguin(object):
...     def __init__(self, name, mood, id=None):
...         self.name = name
...         self.mood = mood
...         self.id = id
...     def __repr__(self):
...         return '< %s the %s penguin >' % (self.name, self.mood)
...
>>> class Goose(object):
...     def __init__(self, name, favorite_penguin, id=None):
...         self.name = name
...         self.favorite_penguin = favorite_penguin
...         self.id = id
...     def __repr__(self):
...         template = '< %s, the goose that likes %s >'
...         return template % (self.name, repr(self.favorite_penguin))
...
>>> grace = Goose('grace', Penguin('penny', 'fat'))
>>> gale = Goose('gale', Penguin('prince', 'cool'))
>>> ginger = Goose('ginger', Penguin('puck', 'boring'))

```

## The JSON session manager
```python
query_tools.JSONEncoder(ModelType)
```
... constructs a json session manager where `ModelType` is the type to be 
encoded. JSON sessions are adaptors to the python json libs.
```python
>>> import query_tools
>>> goose_json_encoder = query_tools.JSONEncoder(Goose)
>>> with goose_json_encoder.make_session() as session:
...     json_data = session.add_all((grace, gale, ginger))
...     print(json_data) # doctest: +NORMALIZE_WHITESPACE
[ 
  {
    "favorite_penguin": {
      "id": null,
      "mood": "fat",
      "name": "penny"
    },
    "id": null,
    "name": "grace"
  },
  {
    "favorite_penguin": {
      "id": null,
      "mood": "cool",
      "name": "prince"
    },
    "id": null,
    "name": "gale"
  },
  {
    "favorite_penguin": {
      "id": null,
      "mood": "boring",
      "name": "puck"
    },
    "id": null,
    "name": "ginger"
  }
]

```

## The SQLAlchemy session manager
```python
query_tools.SQLAlchemy(sqla_metadata, materialized_mappers=None)
```

## The CSV session manager
```python
query_tools.CSVEncoder(model_aggregate_map)
```
... constructs a csv session manager where `model_aggregate_map` is a 
`mapping_tools.Mapper` instance with a map method that returns tabular
instances of the model objects.
```python
>>> class GooseAggregate(object):
...     def __init__(self, name, favorite_penguin_name, favorite_penguin_mood,
...                  favorite_penguin_id=None, id=None):
...         self.name = name
...         self.favorite_penguin_name = favorite_penguin_name
...         self.favorite_penguin_mood = favorite_penguin_mood
...         self.favorite_penguin_id = favorite_penguin_id
...         self.id = id
...     def __repr__(self):
...         template = '< %s the goose has a %s penguin mood >' 
...         return template % (self.name, self.favorite_penguin_mood)
...
>>> import mapping_tools
>>> penguin_projection = mapping_tools.make_projection(Penguin)
>>> goose_aggregate_map = mapping_tools.Mapper(GooseAggregate, {
...     ('name', 'id'):mapping_tools.identity,
...     'favorite_penguin':penguin_projection})
>>> goose_csv_encoder = query_tools.CSVEncoder(goose_aggregate_map)
>>> with goose_csv_encoder.make_session() as session:
...     session.add_all((grace, gale, ginger)) # doctest: +NORMALIZE_WHITESPACE
favorite_penguin_id,favorite_penguin_name,favorite_penguin_mood,name,id
,penny,fat,grace,
,prince,cool,gale,
,puck,boring,ginger,

```
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

Encoder sessions handle objects:
```python
class MyEncoderSession:
    def add_all(self, objects):
        ...
```

Encoder and repository sessions are constructed by session managers:
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
comparison operator.
```python
query_tools.Conjuction(conjuction, criteria)
```
... where `conjuction` interprets the conjuction to be used and `criteria` is
an iterator of criteria.
```python
conjuction.__iter__(self)
```
... returns iter(self.criteria)

