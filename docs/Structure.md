## Project Structure

**Middlewares**
- Under `crm.middlewares`
- More info about [Middlewares](Middlewares.md)


**Custom Command lines**
- Under `crm.cli`
- More info about [Commands](Commands.md)

**Custom Events**
- Under `crm.events`
- More info about [DB Events](DBEvents.md)

**Admin application**
- Under `flask.apps.admin`
- More info about [Admin app](AdminInterface.md)

**Flask sub application**
- Any package under `crm.apps`
- Main modules for any sub app (except the [Admin app](AdminInterface.md)) are:
    - `models.py` for models definitions. Please follow [These conventions](Models.md) when defining your own models
    - `views.py` for HTTP end points definitions. . Please follow [These conventions](Views.md) when defining your own models
        - To add an HTTP end point, you put your code in a function inside `views.py` file in some app decorated by `@app.route`
            ```
            @app.route('/api', methods=["POST"])
            def api():
                pass

            ```
    - `graphql` package for [graphql](graphql.org/learn/) To expose `graphql` mutations & queries for this sub app.
        Please follow [These conventions](GraphqlAdvanced.md)
        - Put types in module `types.py`
        - Put arguments in module `arguments.py`
        - Put queries in module `queries.py`
        - Put mutations in module `mutations.py`


**Main app**
- [Flask](flask.pocoo.org/) Main entry point is ```app.py``` in the root directory
- It imports actual [Flask](flask.pocoo.org/) app :: `crm.app`
    - `crm.app` is defined in `crm/__init__.py` and it's the actual [Flask](flask.pocoo.org/) app
    - `crm/__init__.py` contains code to initialize the app and registering all http endpoints for sub applications in
    `crm.apps` by importig their `views.py` module if found
- It registers all custom commands by doing ```from crm.cli import *```
- It registers all middlewares by doing ```from crm.middlewares import *```
- It registers all db events by doing ```from crm.events import *```
