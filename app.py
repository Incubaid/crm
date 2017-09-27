import sys

from crm import app
from cli import *
from middlewares import *

if len(sys.argv) > 1 and sys.argv[1] != 'loaddata':
    from hooks import *

if __name__ == '__main__':
    app.run(debug=app.debug)
