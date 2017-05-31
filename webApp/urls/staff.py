from django.conf.urls import url

from webApp.views.staff import *

urlpatterns = [
    url(r'^$', List.as_view(), name='staffs'),
    url(r'^token$', Token.as_view(), name='token'),
]
