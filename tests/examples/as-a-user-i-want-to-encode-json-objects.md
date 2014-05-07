As a **user** I want to **encode json objects**.
```python
>>> import query_tools
>>> import test_data.zoo
>>> goose_json_encoder = query_tools.JSONEncoder(test_data.zoo.Goose)
>>> with goose_json_encoder.make_session() as session:
...     json_data = session.add_all(test_data.zoo.geese)
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
