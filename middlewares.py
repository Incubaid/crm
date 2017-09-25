import requests
from jose import jwt

from flask import request, Response
from werkzeug.exceptions import abort
from flask.templating import render_template


from crm import app
from crm.db import db


@app.errorhandler(401)
def custom_401(error):
    return render_template('home/401.html')


@app.before_request
def authenticate():
    caddyoauth = request.cookies.get("caddyoauth")

    if caddyoauth is None:
        abort(401)


@app.before_first_request
def before_first_request():
    from crm.user.models import User
    # if "graphql" in request.url or "api" in request.url:
    #     return
    caddyoauth = request.cookies.get("caddyoauth")

    # Return allowing authenticate() middleware to work
    # Some how abort() in @app.before_first_request raises exception
    # rather than returning 401 gracefully
    if caddyoauth is None:
        return

    claims = jwt.get_unverified_claims(caddyoauth)
    username = claims['username']

    url = "https://itsyou.online/api/users/{}/info".format(username)

    response = requests.get(
        url,
        headers={
            'Authorization': 'bearer {}'.format(caddyoauth)
        }
    )
    response.raise_for_status()
    info = response.json()
    email = info['emailaddresses'][0]['emailaddress']
    userobjs = User.query.filter(User.emails.contains(email))
    phone = info['phonenumbers'][0]['phonenumber']
    if userobjs.count() == 0:
        u = User(
            firstname=info['firstname'] or username,
            lastname=info['lastname'] or username,
            emails=email,
            telephones=phone)

        db.session.add(u)
        db.session.commit()
