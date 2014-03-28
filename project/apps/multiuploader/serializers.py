# -*- coding: utf-8 -*-
import uuid

from rest_framework import serializers
from django.core.files.base import ContentFile

from multiuploader.models import MultiuploaderImage


class MultiuploaderImageSerializer(serializers.ModelSerializer):
    """
    A serializer for ``MultiuploaderImage``.
    """
    image = serializers.SerializerMethodField('get_image')
    caption = serializers.SerializerMethodField('get_caption')
    caption_by = serializers.SerializerMethodField('get_caption_by')
    caption_ev = serializers.SerializerMethodField('get_caption_ev')
    eventslug = serializers.SerializerMethodField('get_eventslug')
    userslug = serializers.SerializerMethodField('get_userslug')
    favorited = serializers.SerializerMethodField('get_favorited')

    class Meta(object):
        model = MultiuploaderImage

    def get_image(self, obj):
        if obj.image:
            return obj.image.url

    def get_caption(self, obj):
        user = self.context['view'].request.user
        if user.is_active:
            profile = user.profile
            if obj.event_date:
                event = obj.event_date.event
                if profile.followed_events.filter(id=event.id).count():
                    return event.title

            if profile.followed_profiles.filter(id=obj.userprofile_id).count():
                return obj.userprofile.get_full_name()

        return ""

    def get_caption_by(self, obj):
        return "by %s" % obj.userprofile.get_full_name()

    def get_caption_ev(self, obj):
        if obj.event_date:
            return "@ %s" %obj.event_date.event.title
        return ""

    def get_eventslug(self, obj):
        if obj.event_date:
            return  "/events/" + obj.event_date.event.slug
        return ""

    def get_userslug(self, obj):
        return "/profile/" + obj.userprofile.slug

    def get_favorited(self, obj):
        user = self.context['view'].request.user
        fav = obj.favorite_by.filter(user=user).count() != 0
        return fav




class Base64ImageField(serializers.Serializer):
    def from_native(self, data, files):
        if data.startswith('data:image'):

            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]

            data = ContentFile(imgstr.decode('base64'), name='%s.%s' % (str(uuid.uuid4()), ext))
            return data
        else:
            raise serializers.ValidationError("File is not an image")


class CoordinateSerializer(serializers.Serializer):
    long = serializers.FloatField(required=False)
    lat = serializers.FloatField(required=False)


class CoordinatedPhotoSerializer(serializers.Serializer):
    """
    Serializer for single MultiuploaderImage with coordinates
    """
    file = Base64ImageField()
    coords = CoordinateSerializer(required=False)
