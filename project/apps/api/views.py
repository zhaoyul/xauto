# -*- coding: utf-8 -*-
#from django.views.decorators.cache import never_cache
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.views import APIView

from event.models import Event
from .serializers import EventSerializer, EventDetailsSerializer


class EventsListView(ListAPIView):
    serializer_class = EventSerializer

    def get_queryset(self):
        search_text = self.request.GET.get('search_text', '')
        return Event.objects.filter(title__startswith=search_text)

class EventDetailsView(RetrieveAPIView):
    serializer_class = EventDetailsSerializer
    model = Event
