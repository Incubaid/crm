import string
import random


def newuid():
    uid = ''.join(random.sample(string.ascii_lowercase + string.digits, 4))
    return uid
