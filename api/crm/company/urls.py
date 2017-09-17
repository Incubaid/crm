from django.conf.urls import url

from company.views import display_company

urlpatterns = [
    url(r'^company/(?P<company_id>\w+)/$', display_company, name='company'),
]
