"""
Custom value types for django-livesettings app.
"""
from django import forms
from django.utils.text import smart_split, unescape_string_literal
from django.utils.safestring import mark_safe

from livesettings.values import Value, NOTSET, PercentValue as BrokenPercentValue

from decimal import Decimal, InvalidOperation

class FixedPercentValue(BrokenPercentValue):

    class field(forms.DecimalField):

        def __init__(self, *args, **kwargs):
            kwargs['required'] = False
            forms.DecimalField.__init__(self, 100, 0, 5, 2, *args, **kwargs)

        class widget(forms.TextInput):
            def render(self, *args, **kwargs):
                attrs = kwargs.pop('attrs', {})
                attrs['size'] = attrs['max_length'] = 6
                return mark_safe(forms.TextInput.render(self, attrs=attrs, *args, **kwargs) + '%')

class ChoiceListValue(Value):

    class field(forms.CharField):
        def __init__(self, *args, **kwargs):
            kwargs['widget'] = forms.Textarea()
            forms.CharField.__init__(self, *args, **kwargs)

    def to_python(self, value):
        if value == NOTSET:
            return []

        out = []
        for pair in value.split('\n'):
            if pair.strip():
                value, name = [a.strip() for a in pair.split(':', 1)]
                out.append([value, name])
        return out

    def to_editor(self, value):
        if value == NOTSET:
            return NOTSET

        out = []
        #return "1:1 day\n2:2 days\n3:3 days\n4:4 days\n5:5 days\n7:7 days\n10:10 days\n14:14 days\n28:28 days"
        return unicode(value)
        for pair in value:
            value, name = pair
            out.append('%s : %s' % (value, name))

        return "\n".join(out)

    def get_db_prep_save(self, value):
        if value == NOTSET:
            return ""

        out = []
        #return "1:1 day\n2:2 days\n3:3 days\n4:4 days\n5:5 days\n7:7 days\n10:10 days\n14:14 days\n28:28 days"

        for pair in value:
            out.append("%s : %s" % (pair[0], pair[1]))
        return "\n".join(out)

class PositiveIntegerListValue(Value):

    class field(forms.CharField):
        pass

    def to_python(self, value):
        if value == NOTSET:
            return []
        return [int(a) for a in value.split(' ')]

    def to_editor(self, value):
        if value == NOTSET:
            return ""
        return " ".join(value)

class DecimalPairListValue(Value):

    class field(forms.CharField):
        def __init__(self, *args, **kwargs):
            kwargs['widget'] = forms.Textarea()
            forms.CharField.__init__(self, *args, **kwargs)

    def to_python(self, value):
        if value == NOTSET:
            return []

        out = []
        for pair in value.split('\n'):
            first, second = [a.strip() for a in pair.split(':', 1)]
            try:
                out.append([Decimal(first), Decimal(second)])
            except InvalidOperation:
                continue
        return out

    def to_editor(self, value):
        if value == NOTSET:
            return ""

        out = []
        return unicode(value)
        for pair in value.split('\n'):
            out.append("%.2f : %.2f" % (pair[0], pair[1]))
        return "\n".join(out)

    def get_db_prep_save(self, value):
        out = []
        for pair in value:
            out.append("%.2f : %.2f" % (pair[0], pair[1]))
        return "\n".join(out)
