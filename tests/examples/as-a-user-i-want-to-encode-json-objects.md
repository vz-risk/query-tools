```python
>>> import query_tools
>>> import model_fixt
>>> import data_fixt
>>> goose_json_encoder = query_tools.JSONEncoder(model_fixt.Goose)
>>> with goose_json_encoder.make_session() as session:
...     json_data = session.add_all(data_fixt.geese)
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
