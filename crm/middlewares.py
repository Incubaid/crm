import requests
from jose.jwt import get_unverified_claims

from flask import g, request

from werkzeug.exceptions import abort
from flask.templating import render_template


from crm import app
from crm.db import db
from crm.user.models import User


@app.errorhandler(401)
def custom_401(error):
    return render_template('home/401.html'), 401


#@app.before_request
def authenticate():
    """
    authenticate user by validating passed JWT token
    Add user info to flask.g (global context)
    so that g.user always hold current logged in user
    """
    jwt = request.cookies.get('caddyoauth')
    if jwt is None:
        authheader = request.headers.get("Authorization", None)
        if authheader is None or 'Bearer' not in authheader:
            abort(401)
        jwt = authheader.split(" ", 1)[1]  # Bearer JWT
    claims = get_unverified_claims(jwt)

    user = None
    globalid = claims.get("globalid", None)

    if globalid is not None:
        orgid = claims
        users = User.query.filter(
            User.firstname == globalid
        )
        if users.count():
            user = users[0]
        else:
            user = User(
                firstname=globalid)
            db.session.add(user)
    else:
        username = claims.get("username", None)
        if username is None:
            abort(401)
        url = "https://itsyou.online/api/users/{}/info".format(
            username
        )

        response = requests.get(
            url,
            headers={
                'Authorization': 'Bearer {}'.format(jwt)
            }
        )
        info = response.json()
        email = info['emailaddresses'][0]['emailaddress']
        phone = info['phonenumbers'][0]['phonenumber']

        users = User.query.filter(
            User.emails.contains(email),
            User.telephones.contains(phone)
        )
        if users.count():
            user = users[0]
        else:
            user = User(
                firstname=info['firstname'] or username,
                lastname=info['lastname'] or username,
                emails=email,
                telephones=phone)

            db.session.add(user)

    db.session.commit()
    g.user = user
