# This Python file uses the following encoding: utf-8
__author__ = 'xiaohe'

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
]