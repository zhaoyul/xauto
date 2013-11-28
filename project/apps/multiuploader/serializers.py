# -*- coding: utf-8 -*-
from rest_framework import serializers

from multiuploader.models import MultiuploaderImage


class MultiuploaderImageSerializer(serializers.ModelSerializer):
    """
    A serializer for ``MultiuploaderImage``.
    """
    class Meta(object):
        model = MultiuploaderImage
