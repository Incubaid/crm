import random
import datetime
from django.core.exceptions import ValidationError


def generate_uid(model):
    """
    Generates UID for classes (PK)
    :param model: model
    :type model: django.db.models.Model
    :return: 4 characters uid
    :rtype: str
    """
    hex_chars = ['a', 'b', 'c', 'd', 'e', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']


    while True:
        uid = ''.join(random.sample(hex_chars, 4))
        if not model.objects.filter(pk=uid).count():
            return uid


def model_to_dict(model):
    d = {}
    for k, v in model.__dict__.iteritems():
        if k.startswith('_'):
            continue
        d[k] = v
    return d

def validate_epoch(value):
    if value:
        try:
            datetime.datetime.fromtimestamp(value)
        except ValueError:
            raise ValidationError('Not valid epoch')

