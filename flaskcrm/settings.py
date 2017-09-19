import os

DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data'))


# **************
# DO NOT TOUCH *
# **************

exec("from crm.config.%s import *" % os.getenv("env", 'development'))
