from datetime import datetime

import jose
import requests
from flask import session, request
from flask.json import jsonify
from flask.templating import render_template
from jose.jwt import get_unverified_claims
from werkzeug.exceptions import abort

from crm import app
from crm.apps.email.models import Email
from crm.apps.phone.models import Phone
from crm.apps.user.models import User
from crm.apps.user.tasks import update_last_login_time
from crm.db import db
from crm.rq import queue

s = requests.Session()


@app.errorhandler(401)
def custom_401(error):
    # API CALL
    if 'Content-Type' in request.headers and request.headers['Content-Type'].lower() == 'application/json':
        return jsonify(errors=['Not authorized']), 401
    return render_template('home/401.html', message=error.description['message']), 401


@app.before_request
def authenticate():
    """
    authenticate user by validating passed JWT token
    Add user info to flask.g (global context)
    so that g.user always hold current logged in user
    """
    # Already authenticated

    last_login = datetime.now()

    # User is logged in already
    if 'user' in session:
        session['user']['last_login'] = last_login
        queue.enqueue(update_last_login_time, session['user']['id'], last_login)
        return

    # User not logged in
    jwt = request.cookies.get('caddyoauth')

    if jwt is None:
        authheader = request.headers.get("Authorization", None)
        if authheader is None or 'bearer ' not in authheader.lower():
            abort(401, {'message': 'Are you coming from <a href="https://itsyou.online/">IYO</a> If not, please do!'})
        jwt = authheader.split(" ", 1)[1]  # Bearer JWT

    try:
        claims = get_unverified_claims(jwt)
    except jose.exceptions.JWTError:
        abort(401, {'message': 'Are you coming from <a href="https://itsyou.online/">IYO</a> If not, please do!'})

    globalid = claims.get("globalid", None)

    if globalid is not None:
        user = User.query.filter(
            User.username == globalid
        ).first()

        if not user:
            user = User(username=globalid)
    else:
        username = claims.get("username", None)

        if username is None:
            abort(401, {'message': 'Missing username from <a href="https://itsyou.online/">IYO</a>!'})

        url = "https://itsyou.online/api/users/{}/info".format(
            username
        )

        response = s.get(
            url,
            headers={
                'Authorization': 'bearer {}'.format(jwt)
            }
        )

        info = response.json()
        emails = [record['emailaddress'] for record in info['emailaddresses']]
        phones = [record['phonenumber'] for record in info['phonenumbers']]

        if not emails:
            abort(401, {'message': 'Missing Email addresses from <a href="https://itsyou.online/">IYO</a>'})
        if not phones:
            abort(401, {'message': 'Missing Phone numbers from <a href="https://itsyou.online/">IYO</a>'})

        user = User.query.filter(
            User.telephones.any(Phone.telephone.in_(phones)) |\
            (User.emails.any(Email.email.in_(emails))) |\
            (User.username == username)
        ).first()

        email_objs = []
        for e in emails:
            o = Email.query.filter_by(email=e).first()
            if o is None:
                email_objs.append(Email(email=e))
            else:
                email_objs.append(o)

        telephone_objs = []
        for p in phones:
            o = Phone.query.filter_by(telephone=p).first()
            if o is None:
                telephone_objs.append(Phone(telephone=p))
            else:
                telephone_objs.append(o)

        # New user
        if not user:
            user = User(
                username=username,
                firstname=info['firstname'],
                lastname=info['lastname'],
                emails=email_objs,
                telephones=telephone_objs
            )

        # User already in system, Update user info
        elif user:
            # update username
            if username and user.username != username:
                user.username = username

            # update emails
            new_emails = set(emails) - set([e.email for e in user.emails])
            if new_emails:
                email_objs = []
                for e in new_emails:
                    o = Email.query.filter_by(email=e).first()
                    if o is None:
                        email_objs.append(Email(email=e))
                    else:
                        email_objs.append(o)
                user.emails.extend(email_objs)

            # update phones
            new_phones = set(phones) - set([p.telephone for p in user.telephones])
            if new_phones:
                telephone_objs = []
                for p in phones:
                    o = Phone.query.filter_by(telephone=p).first()
                    if o is None:
                        telephone_objs.append(Phone(telephone=p))
                    else:
                        telephone_objs.append(o)
                user.telephones.extend(telephone_objs)

    user.last_login = last_login
    db.session.add(user)
    db.session.commit()

    session['user'] = {
        'username': user.username,
        'firstname': user.firstname,
        'lastname': user.lastname,
        'telephones': [p.telephone for p in user.telephones],
        'emails': [e.email for e in user.emails],
        'id': user.id,
        'last_login': last_login
    }
