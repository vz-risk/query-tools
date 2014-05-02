As a **user** I want to **encode json objects**.
```python
>>> import query_tools
>>> import test_data.zoo
>>> goose_json_encoder = query_tools.JSONEncoder(Goose)
>>> with goose_json_encoder.make_session() as session:
...     goose_json_encoder.add_all(test_data.zoo.geese)

```
