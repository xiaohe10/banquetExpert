from django.conf.urls import include, url

from webApp.views import common
from . import admin, hotel, hotel_branch, desk, staff

urlpatterns = [
    url(r'^$', common.index, name='index'),
    url(r'^admin/', include(admin.urlpatterns, namespace='admin')),
    url(r'^hotel/', include(hotel.urlpatterns, namespace='hotel')),
    url(r'^hotel_branch/', include(hotel_branch.urlpatterns,
                                   namespace='hotel_branch')),
    url(r'^desk/', include(desk.urlpatterns, namespace='desk')),
    url(r'^staff/', include(staff.urlpatterns, namespace='staff')),
]
