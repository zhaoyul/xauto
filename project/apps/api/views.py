# -*- coding: utf-8 -*-
#from django.views.decorators.cache import never_cache
from rest_framework.generics import (ListAPIView, RetrieveAPIView)
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from event.models import Event, EventDate
from .serializers import (EventSerializer, EventDetailsSerializer,
    EventModelSerializer, EventImageSerializer, EventDateSerializer)


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
    Returns Event details
    """
    serializer_class = EventModelSerializer
    model = Event

    def pre_save(self, obj):
        if not obj.author:
            user = self.request.user
            obj.author = user.profile

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