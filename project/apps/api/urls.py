# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url, include

from rest_framework import routers

from .views import (EventsListView, EventDetailsView, FollowEventView,
    EventViewSet, EventDateViewSet, CheckShortLinkView)

router = routers.DefaultRouter()
router.register(r'events', EventViewSet)
router.register(r'dates', EventDateViewSet)

urlpatterns = patterns('',
    url(r'^events/list/$', EventsListView.as_view(), name='events-list'),
    url(r'^events/(?P<pk>\d+)/details/$', EventDetailsView.as_view(),
        name='events-details'),
    url(r'^events/(?P<event_id>\d+)/follow/$', FollowEventView.as_view(),
        name='event-follow'),
    url(r'^events/check-link/$', CheckShortLinkView.as_view(), name='check-link'),
    url(r'^', include(router.urls)),
)