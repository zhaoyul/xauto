from django.conf import settings
from django.http import HttpResponse
from django.utils import simplejson as json
from django.utils.encoding import force_unicode
from django.utils.functional import Promise

from functools import wraps


class LazyEncoder(json.JSONEncoder):
	'''
	Special encoder for lazy translation objects.

	See http://docs.djangoproject.com/en/dev/topics/serialization/#id2
	'''
	def default(self, object):
		if isinstance(object, Promise):
			return force_unicode(object)
		return super(LazyEncoder, self).default(object)

def json_encode(data, *args, **kwargs):
    '''
    Return a string containing the JSON representation of the given data.
    '''
    if settings.DEBUG:
        kwargs = dict({'sort_keys': True, 'indent': 2 }, **kwargs)
    else:
        kwargs = dict({'sort_keys': False, 'indent': None }, **kwargs)

    return json.dumps(data, cls=LazyEncoder, *args, **kwargs)

def json_response(x):
    return HttpResponse(json_encode(x), content_type='application/json; charset=UTF-8')

def json_view(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        res = view(*args, **kwargs)
        if isinstance(res, HttpResponse):
            return res
        return json_response(res)
    return wrapped


def iframe_json_view(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        res = view(*args, **kwargs)
        if isinstance(res, HttpResponse):
            return res
        return HttpResponse('<textarea>%s</textarea>' % json.dumps(res))
    return wrapped
