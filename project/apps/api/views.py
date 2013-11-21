# -*- coding: utf-8 -*-
from rest_framework.generics import ListAPIView

from event.models import Event
from .serializers import EventSerializer


class EventsListView(ListAPIView):
    serializer_class = EventSerializer

    def get_queryset(self):
        search_text = self.request.GET.get('search_text', '')
        return Event.objects.filter(title__startswith=search_text)