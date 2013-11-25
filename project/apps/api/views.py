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

    def list(self, request, *args, **kwargs):
        self.object_list = self.filter_queryset(self.get_queryset())

        # Default is to allow empty querysets.  This can be altered by setting
        # `.allow_empty = False`, to raise 404 errors on empty querysets.
        if not self.allow_empty and not self.object_list:
            warnings.warn(
                'The `allow_empty` parameter is due to be deprecated. '
                'To use `allow_empty=False` style behavior, You should override '
                '`get_queryset()` and explicitly raise a 404 on empty querysets.',
                PendingDeprecationWarning
            )
            class_name = self.__class__.__name__
            error_msg = self.empty_error % {'class_name': class_name}
            raise Http404(error_msg)

        # Switch between paginated or standard style responses
        page = self.paginate_queryset(self.object_list)
        if page is not None:
            serializer = self.get_pagination_serializer(page)
        else:
            serializer = self.get_serializer(self.object_list, many=True)

        # We must return dictionary, because angular expected this format.
        #TODO Maybe we can change expected format for my events page.
        dict_data = {}
        for index, event in enumerate(serializer.data, start=1):
            dict_data.update({index: event})

        return Response(dict_data)