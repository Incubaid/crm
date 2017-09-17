from django.dispatch import Signal

contact_added = Signal(providing_args=["request", "data"])
contact_updated = Signal(providing_args=["request", "data"])
contact_deleted = Signal(providing_args=["request", "data"])
