from django import forms

import re

# Reference: http://stackoverflow.com/questions/2639582/python-small-regex-problem
YOUTUBE_URL_REGEX = re.compile("(?:/v/|/watch\?v=|/watch#!v=)([-\w]+)")
YOUTUBE_ID_REGEX = re.compile('[-\w]{11}')

YOUTUBE_URL = 'http://www.youtube.com/v/%s'

class YouTubePreviewForm(forms.Form):
    """
    A simple form for cleaning a submitted youtube url.
    """
    youtube_url = forms.CharField(max_length=100)

    def clean_youtube_url(self):
        value = self.cleaned_data['youtube_url']

        m = YOUTUBE_URL_REGEX.search(value)
        if m:
            value = m.group(1)

        # Validate youtube ID
        m = YOUTUBE_ID_REGEX.match(value)
        if not m:
            raise forms.ValidationError("Invalid YouTube ID entered.")

        
        return YOUTUBE_URL % value
