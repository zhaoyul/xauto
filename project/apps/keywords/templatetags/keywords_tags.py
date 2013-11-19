
from django.template import Library, Node, Variable
from django.utils.dateformat import format
from django.conf import settings
from django.core.urlresolvers import reverse
from django.conf import settings
from django.utils.safestring import mark_safe
from django.views.decorators.cache import cache_page, never_cache
from django.shortcuts import get_object_or_404

from member.models import Statistics
from keywords.models import SubCategKeywords


import datetime
import time
import string
import os
from lib import calutil
import urllib2, urllib
register = Library()


@register.inclusion_tag('keywords/popular_keywords.html', takes_context=True)
def getPopularSearchKeywords(context, mode='provider', maxrec=6, country=settings.DEFAULT_COUNTRY):
    """
    Return  List  of Most popular search By Keywords
    """
    # --- extract Most Popular keyword used  for search -----
    objStat = Statistics.objects.filter(event_stat='search', type_stat= 'keyword', target_stat= mode, country=country).order_by('-count_stat')[:maxrec]
    
    return {
        'keywords': objStat,
    }


@register.inclusion_tag('keywords/popular_keywords_footer.html', takes_context=True)
def getPopularSearchKeywordsFooter(context, mode='provider', maxrec=12, country=settings.DEFAULT_COUNTRY):
    """
    Return  List  of Most popular search By Keywords (for Footer, Multicolumns)
    """
    # --- extract Most Popular keyword used  for search -----
    objStat = Statistics.objects.filter(event_stat='search', type_stat= 'keyword', target_stat= mode, country=country).order_by('-count_stat')[:maxrec]
    
    return {
        'keywords': objStat,
    }



@register.filter()
def getSubLabel(id):
    """
    Return  Sub category label / name
    """
    # --- extract Most Popular keyword used  for search -----
    objStat = SubCategKeywords.objects.get(pk=id)
    return objStat

