import os
from itertools import count
import copy

from django.utils.translation import ugettext as _
from django.forms import widgets
from django.utils.safestring import mark_safe
from django.utils import simplejson as json
from django.core.urlresolvers import reverse
from django.forms.extras.widgets import SelectDateWidget



class ThumbWidget(widgets.FileInput):
    """
    A Image FileField Widget that shows a thumbnail if it has one.
    """
    def __init__(self, attrs={}):
        super(ThumbWidget, self).__init__(attrs)

    def render(self, name, value, attrs=None):
        output = []
        if value and hasattr(value, "url"):
            try:
                from sorl.thumbnail.main import DjangoThumbnail
                thumb = '<img src="%s">' % DjangoThumbnail(value.name, (100,100), ['crop']).absolute_url
            except:
                # just act like a normal file
                output.append('%s <a target="_blank" href="%s">%s</a> <br />%s ' %
                    (_('Currently:'), value.url, os.path.basename(value.path), _('Change:')))
            else:
                output.append('<a class="thumb" target="_blank" href="%s">%s</a> <br />%s ' %
                    (value.url, thumb, _('Change:')))
        output.append(super(ThumbWidget, self).render(name, value, attrs))
        return mark_safe(u''.join(output))


class CalendarWidget(widgets.DateInput):
    def __init__(self, calendar_opts=None, *args, **kwargs):
        self.calendar_opts = calendar_opts or {}
        super(CalendarWidget, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None):
        input_ = super(CalendarWidget, self).render(name, value, attrs)
        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        id_ = final_attrs.get('id', None)
        selector = '#%s' % id_ if id_ else 'input[name=%s]' % name

        opts = json.dumps(self.calendar_opts)

        return mark_safe(input_ + (
            '<script type="text/javascript">' +
                '$(document).ready(function(){' +
                    ('$("%s").datepicker(%s);' % (selector, opts)) +
                '});'
            '</script>'
        ))


class LurkTextInput(widgets.TextInput):
    class Media:
        js = ('js/lurk.js', )

    def __init__(self, lurk_text, *args, **kwargs):
        self.lurk_text = lurk_text
        super(LurkTextInput, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None):
        input_ = super(LurkTextInput, self).render(name, value, attrs)
        final_attrs = self.build_attrs(attrs)
        id_ = final_attrs['id']

        return mark_safe(input_ + (
            '<script type="text/javascript">' +
                '$(document).ready(function(){' +
                    '$("#%s").lurk("%s");' % (id_, self.lurk_text) +
                '});'
            '</script>'
        ))

class SuggestTextInput(widgets.TextInput):
    def __init__(self, suggest_text, *args, **kwargs):
        self.suggest_text = suggest_text
        super(SuggestTextInput, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None):
        value = value or self.suggest_text
        return super(SuggestTextInput, self).render(name, value, attrs)

    def value_from_datadict(self, data, files, name):
        value = data.get(name, None)
        return value if not value == self.suggest_text else ''



class LocationWidget(widgets.HiddenInput):
    is_hidden = False

    def render(self, name, value, attrs=None):
        value = value.json if hasattr(value, 'json') else value
        hidden_field = super(LocationWidget, self).render(name, value, attrs)
        id_ = self.build_attrs(attrs).get('id', '')

        wrapper_id = '%s_wrapper' % id_
        address_id = id_.replace(name, 'address')

        return mark_safe(''.join([
            '<div id="%s">%s</div>' % (wrapper_id, hidden_field),
            '<script type="text/javascript">',
            '$("#%s").geocode({' % wrapper_id,
            '    addressField: $("#%s")' %  address_id,
            '});',
            '</script>',
        ]))


class PlaceSelectWidget(widgets.HiddenInput):
    is_hidden = False

    class Media:
        js = ('js/places-on-map.js',
              'js/places-attachment.js',
              'js/place-selection.js', )

    def render(self, name, value, attrs):
        widget = super(PlaceSelectWidget, self).render(name, value, attrs)
        id_ = self.build_attrs(attrs).get('id', '');

        places = self.choices.queryset
        wrapper_id = '%s-map' % id_
        return mark_safe(''.join((
            widget,
            '<div id="%s" class="map"></div>' % wrapper_id,
            '<script language="javascript">',
            '$(document).ready(function(){',
                'new PlaceSelector({',
                    'placesGetURL: "%s",' % reverse('maps_ajax_places'),
                    'choices: [%s],' % ','.join([str(p.id) for p in places]),
                    'mapWrapperId: "%s",' % wrapper_id,
                    'hiddenInput: $("#%s")' % id_,
                '}).init();'
            '})'
            '</script>'
        )))

class RoundedSelect(widgets.HiddenInput):
    def render(self, name, value, attrs=None, choices=()):
        if value is None: value = ''
        final_attrs = self.build_attrs(attrs, name=name)
        id = final_attrs.get('id')
        choices = choices or self.choices

        output = [
            u'<div id="select-%s" class="select withdropdown %s">' % (id, final_attrs.get('short_name', '')),
                '<span>',
                    unicode(dict(choices)[value] if value else choices[0][1]),
                '</span>'
                '<ul class="dropdown">'
        ] + self.render_options(choices, [value]) + [
                '</ul>',
                super(RoundedSelect, self).render(name, value, attrs),
            '</div>',
            '<script type="text/javascript">',
                '$(function(){ $("#select-%s").dropDown(); });' % id,
            '</script>'
        ]
        return mark_safe(u'\n'.join(output))

    def render_options(self, choices, selected):
        hidden = 'style="display: none;"'
        return ['<li %s><a rel="%s" href="#">%s</a></li>' % (
            (hidden if key in selected else ""), key, unicode(value)
        ) for (key, value) in choices if key]


class RoundedSplitDate(SelectDateWidget):

    def create_select(self, name, field, value, val, choices):
        if 'id' in self.attrs:
            id_ = self.attrs['id']
        else:
            id_ = 'id_%s' % name
        if not (self.required and value):
            choices.insert(0, (0, field[3:].capitalize()))
        local_attrs = self.build_attrs(id=field % id_)
        local_attrs['short_name'] = field[3:] + 's'
        select_html = RoundedSelect().render(field % name, val, local_attrs, choices)
        return select_html


class FieldListWidget(widgets.Widget):
    def __init__(self, widget, attrs=None):
        self.widget = widget
        super(FieldListWidget, self).__init__(attrs)

    def render(self, name, value, attrs=None):
        output = []
        final_attrs = self.build_attrs(attrs)
        id_ = final_attrs.get('id', None)
        for i, val in enumerate(value or [None]):
            if id_:
                final_attrs = dict(final_attrs, id='%s_%s' % (id_, i))
            output.append(self.widget.render(name + '_%s' % i, val, final_attrs))

        return mark_safe(self.format_output(output))

    def value_from_datadict(self, data, files, name):
        values = []
        for i in count():
            value = self.widget.value_from_datadict(data, files, name + '_%s' % i)
            if not value:
                break
            values.append(value)
        return values


    def _has_changed(self, initial, data):
        if initial is None:
            initial = [u'' for x in range(0, len(data))]
        else:
            if not isinstance(initial, list):
                initial = self.decompress(initial)
        for initial, data in zip(initial, data):
            if self.widget._has_changed(initial, data):
                return True
        return False

    def format_output(self, rendered_widgets):
        return u''.join(rendered_widgets)

    @property
    def media(self):
        return self.widget.media

    def __deepcopy__(self, memo):
        obj = super(FieldListWidget, self).__deepcopy__(memo)
        obj.widget = copy.deepcopy(self.widget)
        return obj



