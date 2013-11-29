# -*- coding: utf-8 -*-
from rest_framework import serializers

from multiuploader.models import MultiuploaderImage


class MultiuploaderImageSerializer(serializers.ModelSerializer):
    """
    A serializer for ``MultiuploaderImage``.
    """
    caption = serializers.SerializerMethodField('get_caption')

    class Meta(object):
        model = MultiuploaderImage

    def get_caption(self, obj):
        profile = self.context['view'].request.user.profile
        event = obj.event_date.event

        if profile.followed_events.filter(id=event.id).count():
            return event.title

        if profile.followed_profiles.filter(id=obj.userprofile_id).count():
            return obj.userprofile.get_full_name()

        return ""

