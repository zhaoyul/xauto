from django.db import models
from django import forms

import re

# Reference: http://stackoverflow.com/questions/2639582/python-small-regex-problem
YOUTUBE_URL_REGEX = re.compile("(?:/v/|/watch\?v=|/watch#!v=)([-\w]+)")
YOUTUBE_ID_REGEX = re.compile('[-\w]{11}')

YOUTUBE_URL = 'http://www.youtube.com/v/%s'

class YouTubeField(models.CharField):
    """
    A field storing a youtube url.
    """
    def __init__(self, *args, **kwargs):
        kwargs.update({
            'max_length': 100,
        })
        super(YouTubeField, self).__init__(*args, **kwargs)

    def clean(self, value, model_instance):
        """
        Accept input of a YouTube ID or a full URL.

        Always return value as a full url.
        """
        super(YouTubeField, self).clean(value, model_instance)

        # Did we get a full youtube url?
        m = YOUTUBE_URL_REGEX.search(value)
        if m:
            value = m.group(1)

        # Validate youtube ID
        m = YOUTUBE_ID_REGEX.match(value)
        if not m:
            raise forms.ValidationError("Invalid YouTube ID entered.")

        return YOUTUBE_URL % value

from south.modelsinspector import add_introspection_rules
add_introspection_rules([], ["^video\.fields\.YouTubeField"])
