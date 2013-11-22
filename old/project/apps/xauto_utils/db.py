from django.db import models
from django.db.models.query import EmptyQuerySet
from django.db.models.fields.related import SingleRelatedObjectDescriptor
from django.shortcuts import _get_queryset
from django.contrib.contenttypes.models import ContentType


class AutoSingleRelatedObjectDescriptor(SingleRelatedObjectDescriptor):
  def __get__(self, instance, instance_type=None):
    try:
      return super(AutoSingleRelatedObjectDescriptor, self).__get__(instance, instance_type)
    except self.related.model.DoesNotExist:
      obj = self.related.model(**{self.related.field.name: instance})
      obj.save()
      return obj


class AutoOneToOneField(models.OneToOneField):
  def contribute_to_related_class(self, cls, related):
    setattr(cls, related.get_accessor_name(), AutoSingleRelatedObjectDescriptor(related))


class UpcastSingleRelatedObjectDescriptor(SingleRelatedObjectDescriptor):
    def __get__(self, instance, instance_type=None):
        parent = super(UpcastSingleRelatedObjectDescriptor, self).__get__(instance, instance_type)
        return parent.upcast()


class UpCastOneToOneField(models.OneToOneField):
    '''
    UpCastOneToOneField gets child of related object.
    Use with UpCastModel, instaed of OneToOneField.

    example:

        class MyProfile(UpCastModel):
            user = UpCastOneToOneField(User, primary_key=True)
    '''
    def contribute_to_related_class(self, cls, related):
        setattr(cls, related.get_accessor_name(), UpcastSingleRelatedObjectDescriptor(related))


class UpCastModel(models.Model):
    """
    Base class for models that are ment to be inherited.
    Introduces `upcast` method that returns child instance.
    """
    final_type = models.ForeignKey(ContentType, editable=False)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.final_type = ContentType.objects.get_for_model(type(self))
        super(UpCastModel, self).save(*args, **kwargs)

    def upcast(self):
        if not hasattr(self, '_upcast'):
            if self.final_type.model_class == self.__class__:
                self._upcast = self
            else:
                self._upcast = self.final_type.get_object_for_this_type(id=self.pk)
        return self._upcast

    class Meta:
        abstract = True


def unique_field(queryset_or_model, **kwargs):
    if isinstance(queryset_or_model, models.query.QuerySet):
        queryset = queryset_or_model
    else:
        queryset = queryset_or_model.objects.all()

    if not len(kwargs) == 1:
        raise Exception('unique_field takes one keyword parameter')
    field, value = kwargs.items()[0]
    while True:
        copies = queryset.filter(**{'%s__startswith' % field: value}).count()
        if not copies:
            return value
        value = '%s-%s' % (value, str(copies + 1))


class QuerySetManager(models.Manager):
    use_for_related_fields = True

    def __init__(self, *args, **kwargs):
        super(QuerySetManager, self).__init__(*args, **kwargs)

        class TempEmptyQuerySet(self.queryset_class, EmptyQuerySet):
            pass

        self.empty_queryset_class = TempEmptyQuerySet

    def get_query_set(self):
        return self.queryset_class(self.model, using=self._db)

    def none(self):
        return self._clone(klass=self.empty_queryset_class)


    def __getattr__(self, key):
        return getattr(self.get_query_set(), key)


def queryset_manager(qs_class):
    class Manager(QuerySetManager):
        queryset_class = qs_class
    return Manager()


# --- misc introspection functions ---

def get_table( model ):
    return model._meta.db_table

def get_column( model, field_name ):
    """ For a model field   (A.a)
        returns a string 'table_of_A.column_of_a'

        >>> get_column( User, 'email' )
        'auth_user.email'
    """
    table  = get_table( model )
    column = model._meta.get_field( field_name ).column
    return '%(table)s.%(column)s' % locals()

def get_related_column( model, field_name ):
    """ For a relation   (A.a) -> (B.b)
        returns a string 'table_of_B.column_of_b'

        >>> get_column( CitizenProfile, 'user' )
        'auth_user.id'
    """
    rel    = model._meta.get_field( field_name ).rel
    table  = get_table( rel.to )
    column = rel.get_related_field().column
    return '%(table)s.%(column)s' % locals()

def get_m2m_column( model, field_name ):
    """ For a many-to-many relation   (A.a) <- (b1.B.b2) -> (C.c)
        returns a string 'table_of_B.column_of_b1'

        >>> get_m2m_column( LeadershipCall, 'leaders' )
        'calls_leadershipcall_leaders.leadershipcall_id'
    """
    field  = model._meta.get_field( field_name )
    table  = field.m2m_db_table()
    column = field.m2m_column_name()
    return '%(table)s.%(column)s' % locals()

def get_related_m2m_column( model, field_name ):
    """ For a many-to-many relation   (A.a) <- (b1.B.b2) -> (C.c)
        returns a string 'table_of_B.column_of_b2'

        >>> get_related_m2m_column( LeadershipCall, 'leaders' )
        'calls_leadershipcall_leaders.user_id'
    """
    field  = model._meta.get_field( field_name )
    table  = field.m2m_db_table()
    column = field.m2m_reverse_name()
    return '%(table)s.%(column)s' % locals()

from south.modelsinspector import add_introspection_rules
add_introspection_rules([], ["^placeforpeople\.utils\.db\.AutoOneToOneField"])

def get_object_or_None(klass, *args, **kwargs):
    """
    Uses get() to return an object or None if the object does not exist.

    klass may be a Model, Manager, or QuerySet object. All other passed
    arguments and keyword arguments are used in the get() query.

    Note: Like with get(), a MultipleObjectsReturned will be raised if more than one
    object is found.
    """
    queryset = _get_queryset(klass)
    try:
        return queryset.get(*args, **kwargs)
    except queryset.model.DoesNotExist:
        return None
