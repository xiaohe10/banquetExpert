from django.conf.urls import include, url

from webApp.views import common
from . import super_admin, admin, hotel, hotel_branch, desk, staff, course, live

urlpatterns = [
    url(r'^$', common.index, name='index'),
    url(r'^super_admin/',
        include(super_admin.urlpatterns, namespace='super_admin')),
    url(r'^admin/', include(admin.urlpatterns, namespace='admin')),
    url(r'^hotel/', include(hotel.urlpatterns, namespace='hotel')),
    url(r'^hotel_branch/', include(hotel_branch.urlpatterns,
                                   namespace='hotel_branch')),
    url(r'^desk/', include(desk.urlpatterns, namespace='desk')),
    url(r'^staff/', include(staff.urlpatterns, namespace='staff')),
    url(r'^course/', include(course.urlpatterns, namespace='course')),
    url(r'^live/', include(live.urlpatterns, namespace='live')),
]
