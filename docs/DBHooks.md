## DBHooks

- DB Hooks are functions/callbacks to be executed on some action
like Model update/delete/create
- In order to add a new hook, add it and register it in file ```hooks.py```

**Registering a hook/event**
- List of all [SqlAlchemy events](http://docs.sqlalchemy.org/en/latest/orm/events.html)

- Example:
    ```python
    from sqlalchemy.event import listen

    def my_call_back(mapper, connect, target):
         """
         :param target: Target model
         """
         pass

    listen(klass, 'replace_me_with_event_name', my_call_back)
    ```

**WARNING**
- DB hooks are not working when you execute command ```flask loaddata```
