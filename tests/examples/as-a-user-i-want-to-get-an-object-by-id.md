```
>>> import test_data.zoo
>>> with my_session_manager.make_session() as session:
...     session.get(test_data.zoo.Goose, 1)


```
