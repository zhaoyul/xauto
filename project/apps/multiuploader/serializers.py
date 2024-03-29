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
    image_thumb = serializers.SerializerMethodField('get_image_thumb')
    caption = serializers.SerializerMethodField('get_caption')
    caption_by = serializers.SerializerMethodField('get_caption_by')
    caption_ev = serializers.SerializerMethodField('get_caption_ev')
    eventslug = serializers.SerializerMethodField('get_eventslug')
    userslug = serializers.SerializerMethodField('get_userslug')
    favorited = serializers.SerializerMethodField('get_favorited')
    usericon = serializers.SerializerMethodField('get_usericon')
    username = serializers.SerializerMethodField('get_username')
    event_name = serializers.SerializerMethodField('get_event_name')
    event_date_name = serializers.SerializerMethodField('get_event_date_name')
    location_name = serializers.SerializerMethodField('get_location_name')
    srv_followersCount = serializers.SerializerMethodField('srv_followers_count')
    srv_following = serializers.SerializerMethodField('get_srv_following')

    class Meta(object):
        model = MultiuploaderImage

    def srv_followers_count(self, obj):
        date = obj.event_date
        if date:
            return date.event.followed.count()
        return 0

    def get_event_name(self, obj):
        date = obj.event_date
        if date:
            return date.event.title
        return '---'

    def get_srv_following(self, obj):
        view = self.context['view']
        user = view.request.user
        # TODO: refactor
        try:
            if user.profile.followed_events.filter(id=obj.event_date.event.id).exists():
                return True
        except:
            pass
        return False

    def get_location_name(self, obj):
        date = obj.event_date
        if date:
            return date.location_name
        return u'---'

    def get_event_date_name(self, obj):
        date = obj.event_date
        if date:
            return date.feature_headline
        return u'---'

    def get_usericon(self, obj):
        return obj.userprofile.get_thumbnail(40, 40)

    def get_username(self, obj):
        return obj.userprofile.get_full_name()

    def get_image(self, obj):
        if obj.image:
            return obj.image.url

    def get_image_thumb(self, obj):
        return obj.list_thumb_url()

    def get_caption(self, obj):
        user = self.context['view'].request.user

        if user.is_active and hasattr(user, "profile"):
            profile = user.profile
            if obj.event_date:
                event = obj.event_date.event
                if profile.followed_events.filter(id=event.id).exists():
                    return event.title

            if profile.followed_profiles.filter(id=obj.userprofile_id).exists():
                return obj.userprofile.get_full_name()

        return u""

    def get_caption_by(self, obj):
        return u"by %s" % obj.userprofile.get_full_name()

    def get_caption_ev(self, obj):
        if obj.event_date:
            return u"@ %s" % obj.event_date.event.title
        return ""

    def get_eventslug(self, obj):
        if obj.event_date:
            return "/events/" + obj.event_date.event.slug
        return ""

    def get_userslug(self, obj):
        return "/profile/" + obj.userprofile.slug

    def get_favorited(self, obj):
        user = self.context['view'].request.user
        if user.is_active:
            fav = obj.favorite_by.filter(user=user).exists()
            return fav
        else:
            return False


class Base64ImageField(serializers.Serializer):
    def from_native(self, data, files):
        if data.startswith('data:image'):
            fmt, imgstr = data.split(';base64,')
            ext = fmt.split('/')[-1]

            data = ContentFile(imgstr.decode('base64'), name='%s.%s' % (str(uuid.uuid4()), ext))
            return data
        else:
            raise serializers.ValidationError("File is not an image")


class CoordinateSerializer(serializers.Serializer):
    lon = serializers.FloatField(required=False)
    lat = serializers.FloatField(required=False)


class CoordinatedPhotoSerializer(serializers.Serializer):
    """
    Serializer for single MultiuploaderImage with coordinates
    """
    file = Base64ImageField()
    coords = CoordinateSerializer(required=False)
