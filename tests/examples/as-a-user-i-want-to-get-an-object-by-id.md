```
>>> import fixture_model
>>> with my_session_manager.make_session() as session:
...     session.get(fixture_model.Goose, 1)
< grace, the goose that likes < penny the fat penguin > >

```
