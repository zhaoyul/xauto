# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from .views import EventsListView


urlpatterns = patterns('',
    url(r'^events/$', EventsListView.as_view(), name='events-list'),
)