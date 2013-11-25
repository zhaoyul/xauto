# -*- coding: utf-8 -*-
#from django.views.decorators.cache import never_cache
from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import clone_request
import warnings
from rest_framework.generics import ListAPIView

from event.models import Event
from .serializers import EventSerializer


class EventsListView(ListAPIView):
    serializer_class = EventSerializer

    def get_queryset(self):
        search_text = self.request.GET.get('search_text', '')
        return Event.objects.filter(title__startswith=search_text)