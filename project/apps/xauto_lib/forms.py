from widgets import ReadOnlyWidget, EmailInput

from django import forms
from django.forms.forms import BoundField
from django.template import Context, loader
from django.utils.safestring import mark_safe

import re

class HTML5BoundField(BoundField):
    """
    """
    def as_widget(self, widget=None, attrs=None, **kwargs):
        if attrs is None:
            attrs = {}
        if self.field.required:
            attrs['required'] = 'required'
        if getattr(self.field, 'max_length', None):
            attrs['maxlength'] = self.field.max_length
        if getattr(self.field, 'min_length', None):
            attrs['minlength'] = self.field.min_length
        if getattr(self.field, 'regex', None):
            attrs['pattern'] = self.field.regex.pattern

        if not widget:
            widget = self.field.widget
        if self.field.__class__ == forms.EmailField and widget.__class__ != EmailInput:
            widget = EmailInput()

        if 'class' not in attrs:
            attrs['class'] = 'v%s' % self.field.__class__.__name__
        attrs['class'] += ' ' + widget.attrs.get('class', '')
        if widget.attrs.has_key('prompt') or widget.attrs.has_key('placeholder'):
            attrs['class'] += ' prompt'

        html = super(HTML5BoundField, self).as_widget(widget=widget, attrs=attrs, **kwargs)
        return html

    def label_tag(self, **kwargs):
        contents = super(HTML5BoundField, self).label_tag(**kwargs)
        m = re.sub(r'(<label[^>]+>)(.+)</label>', r'\1<span>\2</span></label>', contents)
        return mark_safe(contents)

    def is_checkbox(self):
        return self.field.__class__ == forms.BooleanField

    def is_teaxarea(self):
        return self.field.__class__ == self.field.widget.__class__ == forms.Textarea

class TemplatedFormMixin(object):
    """
    Mixin class for template-based forms.
    """
    template = 'forms/form.html'

    def output_via_template(self):
        "Helper function for fieldsting fields data from form."
        bound_fields = [HTML5BoundField(self, field, name) for name, field \
                        in self.fields.items()]
        bound_fields_dict = dict([(a.name, a) for a in bound_fields])
        c = Context({
            'form': self,
            'bound_fields': bound_fields,
            'bound_fields_dict':bound_fields_dict
        })
        t = loader.get_template(self.template)
        return t.render(c)

    def __unicode__(self):
        return self.output_via_template()

    def __getitem__(self, name):
        "Returns a BoundField with the given name."
        try:
            field = self.fields[name]
        except KeyError:
            raise KeyError('Key %r not found in Form' % name)
        return HTML5BoundField(self, field, name)

class TemplatedForm(TemplatedFormMixin, forms.Form):
    def __init__(self, *args, **kwargs):
        if kwargs.has_key('template'):
            self.template = kwargs.pop('template')
        super(TemplatedForm, self).__init__(*args, **kwargs)

class TemplatedModelForm(TemplatedFormMixin, forms.ModelForm):
    def __init__(self, member=None, *args, **kwargs):
        if kwargs.has_key('template'):
            self.template = kwargs.pop('template')
        super(TemplatedModelForm, self).__init__(*args, **kwargs)

class TimestampedModelForm(forms.ModelForm):
    """
    A base model form for timestamped models.
    """
    def __init__(self, data=None, files=None, **kwargs):
        super(TimestampedModelForm, self).__init__(data=data, files=files, **kwargs)
        self.fields['created'].widget = ReadOnlyWidget()
        self.fields['modified'].widget = ReadOnlyWidget()
        if kwargs.get('instance', None) is None:
            self.fields['created'].initial = u"--"
            self.fields['modified'].initial = u"--"

class ReordableModelForm(forms.ModelForm):
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.2/jquery-ui.min.js',
        )

class SLBaseForm(TemplatedForm):
    pass

class SLBaseModelForm(TemplatedModelForm):
    """
    A base class for xauto  model forms.
    """
    def __init__(self, data=None, files=None, **kwargs):
        super(SLBaseModelForm, self).__init__(data=data, files=files, **kwargs)

        # TimestampedModel support
        if self.fields.has_key('created'):
            self.fields['created'].widget = ReadOnlyWidget()
            if kwargs.get('instance', None) is None:
                self.fields['created'].initial = u"--"
        if self.fields.has_key('modified'):
            self.fields['modified'].widget = ReadOnlyWidget()
            if kwargs.get('instance', None) is None:
                self.fields['modified'].initial = u"--"

    def clean_created(self):
        if self.instance.pk:
            return self.instance.created
        return None

    def clean_modified(self):
        if self.instance.pk:
            return self.instance.modified
        return None
