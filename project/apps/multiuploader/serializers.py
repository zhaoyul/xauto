# -*- coding: utf-8 -*-
from rest_framework import serializers

from multiuploader.models import MultiuploaderImage


class MultiuploaderImageSerializer(serializers.ModelSerializer):
    """
    A serializer for ``MultiuploaderImage``.
    """
    image = serializers.SerializerMethodField('get_image')
    caption = serializers.SerializerMethodField('get_caption')

    class Meta(object):
        model = MultiuploaderImage

    def get_image(self, obj):
        if obj.image:
            return obj.image.url

    def get_caption(self, obj):
        user = self.context['view'].request.user
        if user.is_active:
            profile = user.profile
            event = obj.event_date.event

            if profile.followed_events.filter(id=event.id).count():
                return event.title

            if profile.followed_profiles.filter(id=obj.userprofile_id).count():
                return obj.userprofile.get_full_name()

        return ""