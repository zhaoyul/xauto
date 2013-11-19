from django import forms
from django.db import models
from django.db.models import OneToOneField
from django.db.models.fields.related import SingleRelatedObjectDescriptor
from django.utils.safestring import mark_safe
from django.utils.text import capfirst

from functools import partial

class StatusComparator(object):
    """
    Instances of the object are attached to models using the StatusField. This
    enables is_<state> attributes on the model.
    """
    def __init__(self, field, compare_to):
        self.field, self.compare_to = field, compare_to

    def __get__(self, instance=None, owner=None):
        if instance is None:
            raise AttributeError(
                "The '%s' attribute can only be accessed from %s instances."
                % (self.field.name, owner.__name__))

        value = instance.__dict__[self.field.name]
        return value == self.compare_to

class StatusField(models.CharField):

    def __init__(self, *args, **kwargs):
        choices = kwargs.get('choices')
        kwargs.update({
            'blank': False,
            'max_length': 20,
        })
        if choices:
            self._make_state_flags(choices)
            kwargs['default'] = choices[0][0]

        super(StatusField, self).__init__(*args, **kwargs)

    def get_internal_type(self):
        return 'CharField'

    def contribute_to_class(self, cls, name):
        assert not hasattr(cls._meta, 'has_status_field'), \
            u"Model %s can't have more than one StatusField." % cls.__class__
        super(StatusField, self).contribute_to_class(cls, name)
        setattr(cls._meta, 'has_status_field', True)
        for state, verbose in self.choices:
            setattr(cls, 'is_%s' % state, StatusComparator(self, state))
            setattr(cls, '%s_%s' % (name.upper(), state.upper()), state)

    def _make_state_flags(self, choices):
        for state, name in choices:
            setattr(self, state.upper(), state)

class AutoSlugField(models.SlugField):
    """
    A slug field which generates its value automatically
    """
    def __init__(self, **kwargs):
        kwargs['blank'] = True
        super(AutoSlugField, self).__init__(**kwargs)

# http://bitbucket.org/offline/django-annoying

class AutoSingleRelatedObjectDescriptor(SingleRelatedObjectDescriptor):
    def __get__(self, instance, instance_type=None):
        try:
            return super(AutoSingleRelatedObjectDescriptor, self).__get__(instance, instance_type)
        except self.related.model.DoesNotExist:
            obj = self.related.model(**{self.related.field.name: instance})
            obj.save()
            return obj

class AutoOneToOneField(OneToOneField):
    """
    OneToOneField creates related object on first call if it doesnt exists yet.
    Use it instead of original OneToOne field.
    """
    def contribute_to_related_class(self, cls, related):
        setattr(cls, related.get_accessor_name(), AutoSingleRelatedObjectDescriptor(related))

from django.db import models
from django import forms

# http://djangosnippets.org/snippets/1200/

class MultiSelectFormField(forms.MultipleChoiceField):
    "A form field for use by FieldSelectField."
    def __init__(self, *args, **kwargs):
        self.max_choices = kwargs.pop('max_choices', 0)
        super(MultiSelectFormField, self).__init__(*args, **kwargs)

    def clean(self, value):
        if not value and self.required:
            raise forms.ValidationError(self.error_messages['required'])
        if value and self.max_choices and len(value) > self.max_choices:
            raise forms.ValidationError('You must select a maximum of %s choice%s.'
                    % (apnumber(self.max_choices), pluralize(self.max_choices)))
        return value

class MultiSelectField(models.Field):
    """
    A model form which stores multiple selected options in a text field.
    """
    __metaclass__ = models.SubfieldBase

    def get_internal_type(self):
        return "TextField"

    def get_choices_default(self):
        return self.get_choices(include_blank=False)

    def formfield(self, **kwargs):
        # don't call super, as that overrides default widget if it has choices
        defaults = {'required': not self.blank,
                    'label': capfirst(self.verbose_name),
                    'help_text': self.help_text,
                    'choices': self.choices}
        if self.has_default():
            defaults['initial'] = self.get_default()
        defaults.update(kwargs)
        return MultiSelectFormField(**defaults)

    def get_db_prep_value(self, value, connection=None, prepared=False):
        if isinstance(value, basestring):
            return value
        elif isinstance(value, list):
            return ",".join(value)

    def to_python(self, value):
        if isinstance(value, list):
            return value
        elif value==None:
            return ''
        return value.split(",")

    def contribute_to_class(self, cls, name):
        super(MultiSelectField, self).contribute_to_class(cls, name)
        if self.choices:
            func = lambda self, fieldname = name, choicedict = dict(self.choices):",".join([choicedict.get(value,value) for value in getattr(self,fieldname)])
            setattr(cls, 'get_%s_display' % self.name, func)

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value)

    def validate(self, value, model_instance):
        if not self.editable:
            # Skip validation for non-editable fields.
            return
        for val in value:
            for option_key, option_value in self.choices:
                if val == option_key:
                    return
            raise exceptions.ValidationError(self.error_messages['invalid_choice'] % val)

        if not value and not self.blank:
            raise exceptions.ValidationError(self.error_messages['blank'])

from south.modelsinspector import add_introspection_rules
add_introspection_rules([], [
    '^xauto\.lib\.fields\.StatusField',
    '^xauto\.lib\.fields\.AutoOneToOneField',
    '^xauto\.lib\.fields\.MultiSelectField',
])
