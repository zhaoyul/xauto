# -*- coding: utf-8 -*-
from rest_framework import serializers

from event.models import Event


class EventSerializer(serializers.ModelSerializer):
    about = serializers.SerializerMethodField('get_about')
    venue = serializers.Field(source='venue.venue')
    city = serializers.Field(source='venue.city')
    state = serializers.Field(source='venue.state')
    country = serializers.Field(source='venue.country')
    #photo = serializers.Field(source='main_image.image')
    photo = serializers.SerializerMethodField('get_photo')

    class Meta:
        model = Event
        fields = ('id', 'title', 'about', 'venue', 'city', 'state', 'country',
            'photo')

    def get_about(self, obj):
        return obj.description

    def get_photo(self, obj):
        return obj.EVENT_IMAGE()
        image = obj.getEventImage()
        if image:
            return image.image

