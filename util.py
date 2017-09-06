import string, random

def newuid():
    uid = ''.join(random.sample(string.ascii_letters+string.digits, 4))
    return uid