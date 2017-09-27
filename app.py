from crm import app
from cli import *
from middlewares import *
from hooks import *

if __name__ == '__main__':
    app.run(debug=app.debug)
