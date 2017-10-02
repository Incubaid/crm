from flask.templating import render_template

from crm import app


@app.route('/')
def hello_world():
    return render_template('home/index.html')
