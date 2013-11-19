import os, re
import urllib2
import urlparse
try:
    from urlparse import parse_qs
except ImportError:
    from cgi import parse_qs
    urlparse.parse_qs = parse_qs

from django.core.exceptions import ValidationError
from django.template.defaultfilters import filesizeformat


class FileSizeValidator(object):
    def __init__(self, max_size):
        self.max_size = max_size

    def __call__(self, value):
        if value.size > self.max_size:
            raise ValidationError('File is too big, %s max please' %
                                  filesizeformat(self.max_size))

class FileExtensionValidator(object):
    def __init__(self, extensions):
        self.extensions = [('.%s' % e if e and not e.startswith('.') else e)
                           for e in extensions]

    def __call__(self, value):
        if not os.path.splitext(value.name)[1] in self.extensions:
            raise ValidationError("Files with this extension are not allowed.")

def get_youtube_id(url):
    """
    >>> get_youtube_id('http://www.youtube.com/watch?v=nN_LtC-evew')
    'nN_LtC-evew'
    >>> get_youtube_id('http://www.youtube.com/watch?v=2vSkFIscyCk&feature=player_embedded')
    '2vSkFIscyCk'
    >>> get_youtube_id('http://www.youtube.com/user/YaleCourses#p/c/18B9F132DFD967A3/1/fVErdGUN_Jk')
    'fVErdGUN_Jk'
    >>> get_youtube_id('http://www.youtube.com/user/SuperKakashiSenpai#p/u/8/thzCu2TlKXo')
    'thzCu2TlKXo'
    >>> get_youtube_id('http://www.youtube.com/user/YaleUniversity#p/search/0/RX9Lssc5Rso')
    'RX9Lssc5Rso'
    """
    if not url.startswith('http://'):
        url = 'http://' + url

    data = urlparse.urlsplit(url)

    if data.netloc != 'www.youtube.com':
        return

    query = urlparse.parse_qs(data.query)

    if 'v' in query:
        return query['v'][0]
    
    possibilities = []
    for x in [data.path, data.fragment]:
        for t in re.split('[^a-zA-Z0-9_-]', x):
            if len(t) == 11:
                possibilities.append(t)

    if len(possibilities) == 1:
        return possibilities[0]
    elif possibilities > 0:
        for possible_id in possibilities:
            try:
                urllib2.urlopen(
                    'http://gdata.youtube.com/feeds/api/videos/%s' % possible_id)
            except urllib2.HTTPError:
                pass
            else:
                return possible_id


class VideoValidator(object):
    def __call__(self, value):
        if not get_youtube_id(value):
            raise ValidationError('Incorrect link')

class AbsoluteURL(object):
    def __call__(self, value):
        if value.startswith('http://'):
            value = 'http://%s' % value
        if not value.endswith('/'):
            value = '%s/'
        return value
