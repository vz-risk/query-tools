As a **user** I want to **add documents to elasticsearch**.
```python
>>> import query_tools
>>> import test_data.zoo
>>> goose_elasticsearch = query_tools.ElasticSearch(
...     'zoo', {test_data.zoo.Goose:'goose'})
>>> with goose_elasticsearch.make_session() as session:
...     session.add_all(test_data.zoo.geese)

```
