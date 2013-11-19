from django import forms
from django.forms.util import flatatt
from django.utils.html import escape
from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe
from django.contrib.admin.widgets import AdminFileWidget

import datetime

class ReadOnlyWidget(forms.Widget):
    """
    A generic read-only widget.
    """
    def render(self, name, value, attrs):
        final_attrs = self.build_attrs(attrs, name=name)
        if hasattr(self, 'initial'):
            value = self.initial
        if hasattr(self, 'choices'):
            for val, name in self.choices:
                if val == value:
                    value = name
                    break
        if value is None:
            value = "--"
            final_attrs['style'] = 'color: #888'
        elif isinstance(value, datetime.datetime):
            from django.utils import formats
            from django.utils.dateformat import format
            value = formats.date_format(value, 'SHORT_DATETIME_FORMAT')
        return mark_safe(u"<p %s>%s</p>" % (flatatt(final_attrs), escape(value)))

    def _has_changed(self, initial, data):
        return False

#from sorl.thumbnail.main import DjangoThumbnail
#def thumbnail(image_path):
#    t = DjangoThumbnail(relative_source=image_path, requested_size=(200, 200))
#    return u'<img src="%s" alt="%s" />' % (t.absolute_url, image_path)

class AdminImageWidget(AdminFileWidget):
    """
    A FileField Widget that displays an image instead of a file path
    if the current file is an image.
    """
    def __init__(self, inline=False, **kwargs):
        self.inline = inline
        super(AdminImageWidget, self).__init__(**kwargs)

    def render(self, name, value, attrs=None):
        output = []
        if value and hasattr(value, 'url'):
            thumbnail = get_thumbnailer(value).get_thumbnail({'size': (80, 80)})
            output.append('<a target="_blank" href="%s"><img src="%s" /></a><br />%s <a target="_blank" href="%s">%s</a><br />%s ' % \
                (value.url, thumbnail.url, _('Currently:'), value.url, value.name, _('Change:')))


            #file_path = '%s%s' % (settings.STATIC_URL, file_name)
            #try:            # is image
            #    Image.open(os.path.join(settings.MEDIA_ROOT, file_name))
            #    output.append('<a target="_blank" href="%s">%s</a><br />%s <a target="_blank" href="%s">%s</a><br />%s ' % \
            #        (file_path, thumbnail(file_name), _('Currently:'), file_path, file_name, _('Change:')))
            #except IOError: # not image
            #    output.append('%s <a target="_blank" href="%s">%s</a> <br />%s ' % \
            #        (_('Currently:'), file_path, file_name, _('Change:')))
            
        output.append(super(AdminFileWidget, self).render(name, value, attrs))
        if self.inline:
            html = u"".join(output)
        else:
            html = '<div style="margin-left: 110px">%s</div>' % u"".join(output)
        return mark_safe(html)

class EmailInput(forms.TextInput):
    input_type = 'email'
