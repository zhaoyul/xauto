from multiuploader.models import MultiuploaderImage

from django.template import Library, Node, Variable
from django.utils.dateformat import format
from django.conf import settings
from django.core.urlresolvers import reverse
from django.conf import settings
from django.utils.safestring import mark_safe
from django.views.decorators.cache import cache_page, never_cache
from django.shortcuts import get_object_or_404


import datetime
import time
import string
import os
from lib import calutil
import urllib2, urllib
register = Library()


@register.inclusion_tag('account/block-images-manage.html', takes_context=True)
def get_image_list(context, user):
    """
    Return  List  of Images for a given user/member
    """
    # --- extract all Images for the selected member -----
    imageList = MultiuploaderImage.objects.filter(userprofile=user)
    
    return {
        'items': imageList,
    }
