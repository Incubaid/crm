import requests
import jose
from flask.json import jsonify
from jose.jwt import get_unverified_claims

from flask import session, request

from werkzeug.exceptions import abort
from flask.templating import render_template


from crm import app
from crm.db import db
from crm.user.models import User


@app.errorhandler(401)
def custom_401(error):
    # API CALL
    if 'Content-Type' in request.headers and request.headers['Content-Type'].lower() == 'application/json':
        return jsonify(errors=['Not authorized']), 401
    return render_template('home/401.html'), 401


@app.before_request
def authenticate():
    """
    authenticate user by validating passed JWT token
    Add user info to flask.g (global context)
    so that g.user always hold current logged in user
    """

    # Already authenticated
    if 'user' in session:
        return

    jwt = request.cookies.get('caddyoauth')

    if jwt is None:
        authheader = request.headers.get("Authorization", None)
        if authheader is None or 'bearer ' not in authheader.lower():
            abort(401)
        jwt = authheader.split(" ", 1)[1]  # Bearer JWT

    try:
        claims = get_unverified_claims(jwt)
    except jose.exceptions.JWTError:
        abort(401)

    globalid = claims.get("globalid", None)

    if globalid is not None:
        orgid = claims

        users = User.query.filter(
            User.username == globalid
        )

        if users.count():
            user = users[0]
        else:
            user = User(username=globalid)
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
                'Authorization': 'bearer {}'.format(jwt)
            }
        )

        info = response.json()
        email = info['emailaddresses'][0]['emailaddress']
        phone = info['phonenumbers'][0]['phonenumber']

        users = User.query.filter(
            (User.username == username) | (User.telephones.contains(
                phone)) | (User.emails.contains(email))
        )

        if users.count():
            user = users[0]
            user.username = username
            if user.emails is None:
                user.emails = email
            else:
                emailslist = [x.strip() for x in user.emails.split(",")]
                if email not in emailslist:
                    emailslist.append(email)
                    user.emails = ",".join(emailslist)
            if user.telephones is None:
                user.telephones = phone
            else:
                phoneslist = [x.strip() for x in user.telephones.split(",")]
                if phone not in phoneslist:
                    phoneslist.append(phone)
                    user.telephones = ",".join(phoneslist)

        else:
            user = User(
                username=username,
                firstname=info['firstname'],
                lastname=info['lastname'],
                emails=email,
                telephones=phone
            )
        db.session.add(user)

    db.session.commit()

    session['user'] = {'username': user.username,
                       'firstname': user.firstname,
                       'lastname': user.lastname,
                       'telephones': user.telephones,
                       'emails': user.emails, 'id': user.id}
