from django.db import models
from django.db.models.fields import IntegerField, FieldDoesNotExist

class OrderingField(IntegerField):
    empty_strings_allowed=False
    def __init__(self, with_respect_to=[], **kwargs):
        self.respect_to = with_respect_to
        kwargs['null'] = False
        #kwargs['editable'] = False
        IntegerField.__init__(self, **kwargs )

    def get_internal_type(self):
        return 'IntegerField'

    def pre_save(self, model_instance, add):
        value = getattr(model_instance, self.attname)
        if value in (0, None):
            value = model_instance._get_next_order_value()
            setattr(model_instance, self.attname, value)
        return super(OrderingField, self).pre_save(model_instance, add)

    def contribute_to_class(self, cls, name):
        assert not hasattr(cls._meta, 'has_ordering_field'), \
            u"A model can't have more than one OrderingField."
        super(OrderingField, self).contribute_to_class(cls, name)
        setattr(cls._meta, 'has_ordering_field', True)
        setattr(cls._meta, 'ordering_field', self)
        setattr(cls, 'get_next_order_value', self._get_next_order_value)

    def _get_next_order_value(self):
        field = getattr(self._meta, 'ordering_field')
        try:
            last = self.__class__._default_manager.order_by('-%s' % field.name)[0]
            try:
                last_order = int(getattr(last, field.attname))
            except:
                last_order = 0
            next = last_order + 1
        except IndexError:
            next = 1
        return next

class OrderableModelMixin(models.Model):
    """
    An abstract model giving models ordering capabilities.

    May be used as a mixin or parent class.
    """
    order = OrderingField()

    class Meta:
        abstract = True

    def _get_next_order_value(self):
        field = getattr(self._meta, 'ordering_field')
        try:
            last = self.__class__._default_manager.order_by('-%s' % field.name)[0]
            try:
                last_order = int(getattr(last, field.attname))
            except:
                last_order = 0
            next = last_order + 1
        except IndexError:
            next = 1
        return next

    def _move_up_or_down(self, is_up=True):
        field = getattr(self._meta, 'ordering_field')
        filter = [(f.name, getattr(self, f.attname)) for f in field.respect_to]
        filter.append(('%s%s' % (field.name, is_up and '__lt' or '__gt'), getattr(self, field.attname)))
        order = '%s%s' % (is_up and '-' or '', field.name)
        try:
            a = self.__class__._default_manager.filter(**dict(filter)).order_by(order)[0]
        except IndexError:
            pass
        else:
            a.order, self.order = self.order, a.order
            a.save()
            self.save()

    def reorder(self):
        objs = list(self.__class__.objects.all())
        s = []
        if objs[0] != self:
            s.append('<a href="%s/move/up/">Up</a>' % self.id)
        if objs[-1] != self:
            s.append('<a href="%s/move/down/">Down</a>' % self.id)
        if len(s) > 1:
            s.insert(1, '/')
        return '&nbsp;'.join(s)
    reorder.short_description = 'order'
    reorder.allow_tags = True
    reorder.admin_order_field = 'order'

from south.modelsinspector import add_introspection_rules
rules = [
  (
    (OrderingField,),
    [],
    {
        "with_respect_to": ["respect_to", {'default': []}],
    },
  )
]
add_introspection_rules(rules, ["^xauto_lib\.orderable\.OrderingField"])
