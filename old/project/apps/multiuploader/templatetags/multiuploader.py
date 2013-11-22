from django import template
from django.conf import settings

register = template.Library()

@register.inclusion_tag('multiuploader/multiuploader_main.html', takes_context=True)
def multiupform(context, member, mode='event'):
    return {
        'static_url':settings.MEDIA_URL,
        'member': member,
        'category_image': mode,
    }