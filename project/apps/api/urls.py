# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url, include

from rest_framework import routers

from .views import (EventsListView, EventDetailsView, FollowEventView,
    EventViewSet, EventDateViewSet, CheckShortLinkView, UserProfileViewSet,
    FollowProfileView, StreamListView, FavoritePictureView, ReportPictureView,
    ProfileFavoritesListView, ProfileMyPhotosListView, RegistrationView,
    LoginView, LogoutView, CurrentUserView, ActivateView, ResetPasswordView,
    ChangePasswordView, CheckUsernameView, AlbumPhotosUploader,
    ConfigurationView, CoordinatedPhotoUploader)

router = routers.DefaultRouter()
router.register(r'events', EventViewSet)
router.register(r'dates', EventDateViewSet)
router.register(r'profiles', UserProfileViewSet)

urlpatterns = patterns('',
    url(r'^configuration/$', ConfigurationView.as_view(), name='configuration'),
    url(r'^events/list/$', EventsListView.as_view(), name='events-list'),
    url(r'^events/(?P<slug>[-\w]+)/details/$', EventDetailsView.as_view(),
        name='events-details'),
    url(r'^events/(?P<slug>[-\w]+)/follow/$', FollowEventView.as_view(),
        name='event-follow'),
    url(r'^register/$', RegistrationView.as_view(), name='profiles-register'),
    url(r'^activate/(?P<activation_key>\w+)/$',
        ActivateView.as_view(), name='activate-profile'),
    url(r'^reset_password/$', ResetPasswordView.as_view(),
        name='reset-password'),
    url(r'^change_password/(?P<activation_key>\w+)/$',
        ChangePasswordView.as_view(), name='change-password'),
    url(r'^login/$', LoginView.as_view(), name='api-login'),
    url(r'^logout/$', LogoutView.as_view(), name='api-logout'),
    url(r'^current-user/$', CurrentUserView.as_view(), name='api-current-user'),
    url(r'^profiles/(?P<slug>[-\w]+)/follow/$', FollowProfileView.as_view(),
        name='profile-follow'),
    url(r'^profiles/pictures/$', ProfileMyPhotosListView.as_view(),
        name='profile-pictures'),
    url(r'^profiles/favorites-list/$', ProfileFavoritesListView.as_view(),
        name='profile-favorites'),
    url(r'^events/check-link/$', CheckShortLinkView.as_view(),
        name='check-link'),
    url(r'^profiles/check-username/$', CheckUsernameView.as_view(),
        name='check-username'),
    url(r'^stream/$', StreamListView.as_view(), name='stream'),
    url(r'^stream/upload/$', AlbumPhotosUploader.as_view(), name='stream-upload'),
    url(r'^pictures/upload/$',
        CoordinatedPhotoUploader.as_view(), name='picture-upload'),
    url(r'^pictures/(?P<picture_id>\d+)/favorite/$',
        FavoritePictureView.as_view(), name='picture-favorite'),
    url(r'^pictures/(?P<picture_id>\d+)/report/$',
        ReportPictureView.as_view(), name='picture-report'),
    url(r'^', include(router.urls)),
)
