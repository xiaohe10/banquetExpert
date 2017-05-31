from django.conf.urls import include, url

from webApp.views import common
from . import hotel, hotel_branch, room, staff

urlpatterns = [
    url(r'^$', common.index, name='index'),
    url(r'^hotel/', include(hotel.urlpatterns, namespace='hotel')),
    url(r'^hotel_branch/', include(hotel_branch.urlpatterns,
                                   namespace='hotel_branch')),
    url(r'^room/', include(room.urlpatterns, namespace='room')),
    url(r'^staff/', include(staff.urlpatterns, namespace='staff')),
]
