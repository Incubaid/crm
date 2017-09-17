from .signals import contact_added, contact_deleted, contact_updated

from django.dispatch import receiver
from django.core.cache import cache


@receiver(contact_added)
def contact_added_receiver(sender, **kwargs):
    request= kwargs.get('request')
    data = kwargs.get('data')
    cache.set(request.epoch, {
        'data': data,
        'username': request.user.username,
        'email': getattr(request.user, 'email', ''),
    })


@receiver(contact_deleted)
def contact_deleted_receiver(sender, **kwargs):
    print("contact_deleted!")


@receiver(contact_updated)
def contact_updated_receiver(sender, **kwargs):
    request = kwargs.get('request')
    data = kwargs.get('data')
    cache.set(request.epoch, {
        'data': data,
        'username': request.user.username,
        'email': getattr(request.user, 'email', ''),
        'action': 'update'
    })