# -*- coding: utf-8 -*-
from rest_framework import serializers

from event.models import Event


class EventSerializer(serializers.ModelSerializer):
    photo = serializers.Field(source='main_image')
    venue = serializers.SerializerMethodField('get_venue')
    addr1 = serializers.SerializerMethodField('get_addr1')
    addr2 = serializers.SerializerMethodField('get_addr2')
    city = serializers.SerializerMethodField('get_city')
    state = serializers.SerializerMethodField('get_state')
    zipcode = serializers.SerializerMethodField('get_zip')
    country = serializers.SerializerMethodField('get_country')
    srv_followersCount = serializers.SerializerMethodField('srv_followers_count')
    srv_photosCount = serializers.SerializerMethodField('srv_photos_count')

    class Meta:
        model = Event
        fields = ('id', 'title', 'about', 'eventSize', 'srv_followersCount',
            'srv_photosCount', 'photo', 'venue', 'addr1', 'addr2', 'city',
            'state', 'zipcode', 'country')

    def get_venue(self, obj):
        nearest_date = obj.get_nearest_date()
        if nearest_date:
            return nearest_date.location_name
        return ""

    def get_addr1(self, obj):
        nearest_date = obj.get_nearest_date()
        if nearest_date:
            return nearest_date.address_1
        return ""

    def get_addr2(self, obj):
        nearest_date = obj.get_nearest_date()
        if nearest_date:
            return nearest_date.address_2
        return ""

    def get_city(self, obj):
        nearest_date = obj.get_nearest_date()
        if nearest_date:
            return nearest_date.city
        return ""

    def get_state(self, obj):
        nearest_date = obj.get_nearest_date()
        if nearest_date:
            return nearest_date.state
        return ""

    def get_zip(self, obj):
        nearest_date = obj.get_nearest_date()
        if nearest_date:
            return nearest_date.zipcode
        return ""

    def get_country(self, obj):
        nearest_date = obj.get_nearest_date()
        if nearest_date:
            return nearest_date.country
        return ""

    def srv_followers_count(self, obj):
        return obj.followed.count()

    def srv_photos_count(self, obj):
        return obj.event_upload_images.count()
