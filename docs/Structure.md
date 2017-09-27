## Project Structure

- We use [Flask](flask.pocoo.org/)

**Main app**
- Flask likes to have an entry point to any web application
- Our main entry point is ```app.py```
- ```app.py``` is used by flask dev server to run the web app or by uwsgi
that's why you need to make ```export FLASK_APP=app.py``` before you run
flask commands or run the web application
- Inside ```app.py``` module Aactual flask application is called ```app```
so the main entry point is ```app:app```
- ```app.py``` module imports ```crm.app``` which is the actual flask application defined in
```crm/__init__.py``` and where all logic of initializing application happens
- module ```app.py``` imports ```from cli import *``` to register custom flask commands
- module ```app.py``` imports ```from middlewares import *``` to register middlewares
- module ```app.py``` imports ```from hooks import *``` to register DB hooks

**Flask sub applications**
- under package ```crm``` we have many sub applications i.e ```crm.contact```
- if you want to register models for a sub application automatically, put them in a file called ```models.py```
- if you want to register http actions for a sub application automatically, put them in a file called ```views.py```
- More about [Models](Models.md)
- More about [Views](Views.md)
