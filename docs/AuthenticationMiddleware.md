## Authentication
- We don't support authentication on CRM level unfortuantely, we depend on 3rd party [oauth](https://oauth.net/) services
like [IYO](https://itsyou.online) to do so
- If you're going to implement your own authentication mechanism, then you need a [Middleware](https://en.wikipedia.org/wiki/Middleware) to do so
- you can [Define your own middlewares](Middlewares.md) in `crm.middlewares` package
- By default in production mode we have  [IYO](https://itsyou.online) authentication support using this 2 steps process:
    - we use [Caddy Server](https://caddyserver.com/) with [IYO](https://itsyou.online) to do redirection and authentication for us
    and put a JWT token in request header

    - We use a [Middleware](https://en.wikipedia.org/wiki/Middleware) `crm.middlewares.iyo` to :
        - Validate the JWT token, extract user info out of it
        - If user not in `users` table, we create a new user, otherwise we update user info
        - We set session['user'] entry for that user, so later if we found info in session
        we authorize user directly without hitting the Database
- If you want to run the app without `crm.middlewares.iyo` then before running the app you may do `export EXCLUDED_MIDDLEWARES=iyo`
- All session data are invalidated when you restart the CRM app
    > This done by generating new `app.secret_key` settings for CRM app every time is started

###### Writing your own Authentication middleware

- Put a new middleware in `crm.middlewares` package
- You can get current flask session and request from `flask.session` and`flask.request`
- write a middleare function decorated by `@app.before_request` and hamdle auth lofic there
    ```python
        from crm import app
        from flask import session, request

        @app.before_request
        def my_middleware():
            pass
    ```
