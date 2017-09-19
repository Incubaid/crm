from flask.app import Flask
from flask_admin.helpers import get_url

app = Flask(__name__)
app.config.from_pyfile("../settings.py")

app.secret_key = app.config['SECRET_KEY']

# JINJA extra globals.
app.jinja_env.globals.update(
    getattr=getattr,
    hasattr=hasattr,
    type=type,
    len=len,
    get_url=get_url
)
