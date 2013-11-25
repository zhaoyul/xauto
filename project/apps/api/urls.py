# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from .views import EventsListView, EventDetailsView


urlpatterns = patterns('',
    url(r'^events/$', EventsListView.as_view(), name='events-list'),
    url(r'^events/(?P<pk>\d+)/$', EventDetailsView.as_view(), name='events-details'),
)