# -*- coding: utf-8 -*-
from rest_framework import serializers

from event.models import Event


class EventSerializer(serializers.ModelSerializer):
    photo = serializers.Field(source='main_image')
    srv_followersCount = serializers.SerializerMethodField('srv_followers_count')
    srv_photosCount = serializers.SerializerMethodField('srv_photos_count')
    date_info = serializers.SerializerMethodField('get_date_info')
    author_name = serializers.SerializerMethodField('get_author_name')
    author_photo = serializers.SerializerMethodField('get_author_photo')
    srv_live = serializers.SerializerMethodField('get_srv_live')
    srv_following = serializers.SerializerMethodField('get_srv_following')

    class Meta:
        model = Event
        fields = ('id', 'title', 'about', 'eventSize', 'srv_followersCount',
            'srv_photosCount', 'photo', 'date_info', 'author_name',
            'author_photo', 'srv_live', 'srv_following')

    def srv_followers_count(self, obj):
        return obj.followed.count()

    def srv_photos_count(self, obj):
        return obj.event_upload_images.count()

    def get_author_name(self, obj):
        if obj.author:
            return obj.author.get_full_name()
        return ""

    def get_author_photo(self, obj):
        if obj.author:
            return obj.author.thumbnail_image.url
        return ""

    def get_srv_live(self, obj):
        #TODO Return real value
        return "true"

    def get_srv_following(self, obj):
        #TODO Return real value
        return "true"

    def get_date_info(self, obj):
        nearest_date = obj.get_nearest_date()
        if nearest_date:
            return {
                "date": nearest_date.start_date,
                "startTime": nearest_date.start_date.strftime('%H:%M'),
                "endTime": nearest_date.end_date.strftime('%H:%M'),
                #"location_name": nearest_date.location_name,
                #"addr1": nearest_date.address_1,
                #"addr2": nearest_date.address_2,
                "city": nearest_date.city,
                "state": nearest_date.state,
                #"zip": nearest_date.zipcode,
                "country": nearest_date.country,
                "featureHeadline": nearest_date.feature_headline,
                #"featureDetail": nearest_date.feature_detail,
                "attend_free": nearest_date.attend_free,
                "attend_low": nearest_date.attend_price_from,
                "attend_high": nearest_date.attend_price_to,
                "attend_currency": nearest_date.currency,
                #"exhibit_free": nearest_date.exhibit_free,
                #"exhibit_low": nearest_date.exhibit_price_from,
                #"exhibit_high": nearest_date.exhibit_price_to,
                #"exhibit_currency": nearest_date.currency
            }
        return {
            "date": '',
            "startTime": '',
            "endTime": '',
            "location_name": '',
            "addr1": '',
            "addr2": '',
            "city": '',
            "state": '',
            "zip": '',
            "country": '',
            "featureHeadline": '',
            "featureDetail": '',
            "attend_free": '',
            "attend_low": '',
            "attend_high": '',
            "attend_currency": '',
            "exhibit_free": '',
            "exhibit_low": '',
            "exhibit_high": '',
            "exhibit_currency": '',
        }
