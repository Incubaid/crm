from flask import request

def get_current_claims():
    """
    Get current username from current request
    :return logged in user or guest
    """
    from jose.jwt import get_unverified_claims

    username = 'guest'

    jwt = request.cookies.get('caddyoauth')
    if jwt:
        return get_unverified_claims(jwt)


def get_current_username():
    """
    Get current username from current request
    :return logged in user or guest
    """
    claims = get_current_claims()
    return claims.get('username', None)



def get_current_user():
    import requests
    from crm.user.models import User
    username = get_current_username()
    url = "https://itsyou.online/api/users/{}/info".format(username)
    jwt = request.cookies.get('caddyoauth')

    response = requests.get(
        url,
        headers={
            'Authorization': 'bearer {}'.format(jwt)
        }
    )
    response.raise_for_status()
    info = response.json()
    email = info['emailaddresses'][0]['emailaddress']
    userobjs = User.query.filter(User.emails.contains(email))
    if userobjs.count() == 1:
        return userobjs[0]

