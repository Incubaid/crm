## Middlewares

**What is a middleware**

- A middleware in a web application is a piece of software that runs
before any request in the web application and thus it can do operations
that is global to all/some http actions in your app.
Check [Wikipedia Middleware](https://en.wikipedia.org/wiki/Middleware) for more info

**How to add a middleware in CRM system**

- Just add your middleware module inside the package `crm.middlewares`
- write your middleware logic in a function decorated by `@app.before_first_request` and import `flask.request` to get current request
then middleware is exposed automatically
    ```python
        from crm import app
        from flask import request

        @app.before_request
        def my_middleware():
            pass
    ```

**Example**

CRM authentication is done through a middleware `crm.middlewares.iyo`, please check [Authentication middleware](AuthenticationMiddleware.md)


**How to disable a middleware during development mode**

Before running app, do `export EXCLUDED_MIDDLEWARES=md1,md2,..` where `EXCLUDED_MIDDLEWARES` takes comma separated list of middleware modulenames in `crm.middlewares` package
