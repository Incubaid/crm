from django.conf.urls import url
from views import hell

urlpatterns = [
    url(r'^hello/', hell),
]
