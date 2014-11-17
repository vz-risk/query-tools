```
>>> import model_fixt
>>> with my_session_manager.make_session() as session:
...     session.get(model_fixt.Goose, 1)
< grace, the goose that likes < penny the fat penguin > >

```
