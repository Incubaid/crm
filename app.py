import sys

from crm import app
from crm.cli import *
from crm.middlewares import *


if 'loaddata' not in sys.argv:
    from crm.hooks import *

