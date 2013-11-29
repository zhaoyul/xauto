# -*- coding: utf-8 -*-
from datetime import datetime

#from django.views.decorators.cache import never_cache
from django.db.models import Q

from rest_framework.generics import (ListAPIView, RetrieveAPIView)
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from event.models import Event, EventDate
from event.serializers import (EventSerializer, EventDetailsSerializer,
    EventModelSerializer, EventDateSerializer, AlbumSerializer)
from account.serializers import UserProfileSerializer, UserSerializer
from account.models import UserProfile
from multiuploader.serializers import MultiuploaderImageSerializer
from multiuploader.models import MultiuploaderImage


class EventsListView(ListAPIView):
    """
    Returns Event list
    """
    serializer_class = EventSerializer

    def get_queryset(self):
        search_text = self.request.GET.get('search_text', '')
        queryset = Event.objects.filter(title__startswith=search_text)
        own_events = self.request.GET.get('own_events', False)
        if own_events == 'true':
            queryset = queryset.filter(author=self.request.user.profile)
        return queryset


class EventDetailsView(RetrieveAPIView):
    """
    Returns Event details
    """
    serializer_class = EventDetailsSerializer
    model = Event


class EventViewSet(ModelViewSet):
    """
    Returns Event CRUD methods
    """
    serializer_class = EventModelSerializer
    model = Event

    def pre_save(self, obj):
        if not obj.author:
            obj.author = self.request.user.profile

'''
class EventEditView2(APIView):
    serializer_class = EventModelSerializer
    model = Event

    def post(self, request, *args, **kwargs):
        event = EventModelSerializer(data=request.DATA)
        event_image = EventImageSerializer(data=request.DATA,
                                           files=request.FILES)
        print "???"
        print request.FILES
        if event.is_valid() and event_image.is_valid():
            event_image_object = event_image.save(force_insert=True)
            user = self.request.user
            event.object.author = user.profile
            event.object.main_image = event_image_object
            event.save(force_insert=True)
            return Response(event.data, status=status.HTTP_201_CREATED)

        errors = event.errors
        errors.update(event_image.errors)
        return Response(errors, status=status.HTTP_400_BAD_REQUEST)
'''


class EventDateViewSet(ModelViewSet):
    serializer_class = EventDateSerializer
    model = EventDate


class FollowEventView(APIView):
    """
    Adding current user as follower of event
    """
    def put(self, request, event_id, *args, **kwargs):
        user = request.user
        event = Event.objects.get(id=event_id)
        srv_following = False
        try:
            if user.profile.followed_events.filter(id=event_id).count():
                user.profile.followed_events.remove(event)
            else:
                user.profile.followed_events.add(event)
                srv_following = True

            data = {
                'srv_followersCount': event.followed.count(),
                'srv_following': srv_following
            }

            return Response(data, status=status.HTTP_200_OK)
        except:
            pass
        return Response({}, status=status.HTTP_403_FORBIDDEN)


class CheckShortLinkView(APIView):
    """
    Checks database to determine availability of short link.
    """
    def get(self, request, *args, **kwargs):
        search_text = self.request.GET.get('search_text', '')
        data = {'response': 'Available'}
        if Event.objects.filter(short_link=search_text).count():
            data = {'response': 'Unavailable'}

        return Response(data, status=status.HTTP_200_OK)


class UserProfileViewSet(ModelViewSet):
    serializer_class = UserProfileSerializer
    model = UserProfile

    def pre_save(self, obj):
        user_data = self.request.DATA.get('user', {})

        full_name = user_data.get('full_name', '').split(' ')
        user_data['first_name'] = full_name[0]
        if len(full_name) > 1:
            user_data['last_name'] = ' '.join(full_name[1:])

        user_serializer = UserSerializer(obj.user, data=user_data)

        if user_serializer.is_valid():
            password = user_data.get('password_1', '')
            if password:
                if password == user_data.get('password_2', ''):
                    user_serializer.object.set_password(password)

            user_serializer.save()


class FollowProfileView(APIView):
    """
    Adding current user as follower of Profile
    """
    def put(self, request, profile_id, *args, **kwargs):
        user = request.user
        profile = UserProfile.objects.get(id=profile_id)
        srv_following = False
        try:
            if user.profile.followed_profiles.filter(id=profile_id).count():
                user.profile.followed_profiles.remove(profile)
            else:
                user.profile.followed_profiles.add(profile)
                srv_following = True

            data = {
                'srv_followersCount': profile.followed.count(),
                'srv_following': srv_following
            }

            return Response(data, status=status.HTTP_200_OK)
        except:
            pass
        return Response({}, status=status.HTTP_403_FORBIDDEN)


class ProfileMyPhotosListView(ListAPIView):
    """
    Returns current user photos
    """
    serializer_class = AlbumSerializer

    def get_queryset(self):
        profile = self.request.user.profile
        return EventDate.objects.filter(id__in=
            profile.profile_images.values_list('event_date_id', flat=True))


class ProfileFavoritesListView(ListAPIView):
    """
    Returns favorite images for current user
    """
    serializer_class = MultiuploaderImageSerializer

    def get_queryset(self):
        profile = self.request.user.profile

        return MultiuploaderImage.objects.filter(favorite_by__id=profile.id)


class StreamListView(ListAPIView):
    """
    Returns real-time images from Events or Profiles being followed
    """
    serializer_class = MultiuploaderImageSerializer

    def get_queryset(self):
        profile = self.request.user.profile

        events_ids = Event.objects.filter(
            Q(author_id__in=profile.followed.values_list('id', flat=True)) |
            Q(followed__id=profile.id)
        )
        queryset = MultiuploaderImage.objects.filter(
            Q(event_date__event_id__in=events_ids) &
            Q(event_date__start_date__lt=datetime.now()) &
            Q(event_date__end_date__gt=datetime.now())
        )

        return queryset


class FavoritePictureView(APIView):
    """
    Adding Picture to favorites
    """
    def put(self, request, picture_id, *args, **kwargs):
        user = request.user
        picture = MultiuploaderImage.objects.get(id=picture_id)
        try:
            if user.profile.favorite_images.filter(id=picture_id).count():
                user.profile.favorite_images.remove(picture)
            else:
                user.profile.favorite_images.add(picture)

            return Response({}, status=status.HTTP_200_OK)
        except:
            pass
        return Response({}, status=status.HTTP_403_FORBIDDEN)


class ReportPictureView(APIView):
    """
    Flagging Picture as inappropriate
    """
    def put(self, request, picture_id, *args, **kwargs):
        picture = MultiuploaderImage.objects.get(id=picture_id)
        picture.is_inappropriate = True
        picture.save()

        return Response({}, status=status.HTTP_200_OK)