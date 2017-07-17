from django.conf.urls import include, url

from webApp.views import common
from . import super_admin, admin, hotel, hotel_branch, order, guest, staff, \
    course, live, score, intelligent_ordering

urlpatterns = [
    url(r'^upload/file/', common.upload_android_app, name='upload_file'),
    url(r'^super_admin/',
        include(super_admin.urlpatterns, namespace='super_admin')),
    url(r'^admin/', include(admin.urlpatterns, namespace='admin')),
    url(r'^hotel/', include(hotel.urlpatterns, namespace='hotel')),
    url(r'^hotel_branch/', include(hotel_branch.urlpatterns,
                                   namespace='hotel_branch')),
    url(r'^order/', include(order.urlpatterns, namespace='order')),
    url(r'^guest/', include(guest.urlpatterns, namespace='guest')),
    url(r'^staff/', include(staff.urlpatterns, namespace='staff')),
    url(r'^course/', include(course.urlpatterns, namespace='course')),
    url(r'^live/', include(live.urlpatterns, namespace='live')),
    url(r'^score/', include(score.urlpatterns, namespace='score')),
    url(r'^intelligent_ordering/', include(
        intelligent_ordering, namespace='intelligent_ordering')),
]
