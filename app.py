import sys

from crm import app
from crm.cli import *
from crm.middlewares import *


if 'loaddata' not in sys.argv and 'loadfixtures' not in sys.argv:
    import crm.events
