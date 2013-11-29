# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url, include

from rest_framework import routers

from .views import (EventsListView, EventDetailsView, FollowEventView,
    EventViewSet, EventDateViewSet, CheckShortLinkView, UserProfileViewSet,
    FollowProfileView, StreamListView, FavoritePictureView, ReportPictureView,
    ProfileFavoritesListView, ProfileMyPhotosListView)

router = routers.DefaultRouter()
router.register(r'events', EventViewSet)
router.register(r'dates', EventDateViewSet)
router.register(r'profiles', UserProfileViewSet)

urlpatterns = patterns('',
    url(r'^events/list/$', EventsListView.as_view(), name='events-list'),
    url(r'^events/(?P<pk>\d+)/details/$', EventDetailsView.as_view(),
        name='events-details'),
    url(r'^events/(?P<event_id>\d+)/follow/$', FollowEventView.as_view(),
        name='event-follow'),
    url(r'^profiles/(?P<profile_id>\d+)/follow/$', FollowProfileView.as_view(),
        name='profile-follow'),
    url(r'^profiles/pictures/$', ProfileMyPhotosListView.as_view(),
        name='profile-pictures'),
    url(r'^profiles/favorites-list/$', ProfileFavoritesListView.as_view(),
        name='profile-favorites'),
    url(r'^events/check-link/$', CheckShortLinkView.as_view(), name='check-link'),
    url(r'^stream/$', StreamListView.as_view(), name='stream'),
    url(r'^pictures/(?P<picture_id>\d+)/favorite/$',
        FavoritePictureView.as_view(), name='picture-favorite'),
    url(r'^pictures/(?P<picture_id>\d+)/report/$',
        ReportPictureView.as_view(), name='picture-report'),
    url(r'^', include(router.urls)),
)