def get_current_username():
    """
    Get current username from current request
    :return logged in user or guest
    """
    from flask import request
    from jose.jwt import get_unverified_claims

    username = 'guest'

    jwt = request.cookies.get('caddyoauth')
    if jwt:
        claims = get_unverified_claims(jwt)
        username = claims.get('username') or username
    return username
