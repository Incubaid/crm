from crm import app
from cli import *
from middlewares import *

if __name__ == '__main__':
    app.run(debug=app.debug)
