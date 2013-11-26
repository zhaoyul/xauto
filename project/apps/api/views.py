# -*- coding: utf-8 -*-
#from django.views.decorators.cache import never_cache
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from event.models import Event
from .serializers import EventSerializer, EventDetailsSerializer


class EventsListView(ListAPIView):
    """
    Returns Event list
    """
    serializer_class = EventSerializer

    def get_queryset(self):
        search_text = self.request.GET.get('search_text', '')
        return Event.objects.filter(title__startswith=search_text)


class EventDetailsView(RetrieveAPIView):
    """
    Returns Event details
    """
    serializer_class = EventDetailsSerializer
    model = Event


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