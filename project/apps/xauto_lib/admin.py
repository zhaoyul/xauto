from forms import TimestampedModelForm, SLBaseModelForm
from xauto_lib.models import TimestampedModel

from django.contrib import admin
from django.db import models
from django.forms import MediaDefiningClass
from django.conf.urls import patterns
from django.http import HttpResponseRedirect
from django.utils.safestring import mark_safe
from django_extensions.admin import ForeignKeyAutocompleteAdmin

import re
from functools import partial

from django.contrib.admin.views import main
main.EMPTY_CHANGELIST_VALUE = mark_safe('<span style="color: #aaa">--</span>')

class TimestampedModelAdmin(admin.ModelAdmin):
    """
    A model admin superclass for timestamped models.
    """
    form = TimestampedModelForm

move_regex = r'^(?P<obj_id>\d+)/move/(?P<direction>up|down)/?$'

class ReorderableAdmin(admin.ModelAdmin):
    """
    A model admin superclass for models that can be reordered.
    """
    def get_urls(self):
        urls = super(ReorderableAdmin, self).get_urls()
        my_urls = patterns('',
            (move_regex, self.move),
        )
        return my_urls + urls

    def __call__(self, request, url):
        # Django-1.0.x compatibility
        if url:
            m = re.match(move_regex, url)
            if m:
                return self.move(request, m.group('obj_id'), m.group('direction'))
        return super(ReorderableAdmin, self).__call__(request, url)

    def move(self, request, obj_id, direction):
        if not request.user.has_perm('%s.%s' % (self.model._meta.app_label,
                                                self.model._meta.get_change_permission())):
            raise Unauthorized

        obj = self.get_object(request, obj_id)
        if direction == 'up':
            obj.move_up()
        else:
            obj.move_down()

        return HttpResponseRedirect('../../../')

class SLBaseModelAdminMetaclass(MediaDefiningClass):

    def __getattr__(cls, name):

        def foreign_key_link(instance, field):
            target = getattr(instance, field)
            return u'<a href="../../%s/%s/%d/">%s</a>' % (
                target._meta.app_label, target._meta.module_name, target.id, unicode(target))

        if name[:8] == 'link_to_':
            method = partial(foreign_key_link, field=name[8:])
            method.__name__ = name[8:]
            method.allow_tags = True
            setattr(cls, name, method)
            return getattr(cls, name)

        def show_thumb(instance, field):
            image = getattr(instance, field)
            try:
                return u'<img src="%s" /><br />' % image.extra_thumbnails['admin']
            except:
                return ''

        if name[-6:] == '_thumb':
            method = partial(show_thumb, field=name[:-6])
            method.__name__ = name[:-6]
            method.allow_tags = True
            setattr(cls, name, method)
            return getattr(cls, name)

        raise AttributeError

class SLBaseModelAdmin(ForeignKeyAutocompleteAdmin):
    """
    A model admin base class for xauto models.
    """
    #form = SLBaseModelForm
    __metaclass__ = SLBaseModelAdminMetaclass

    class Media:
        css = {
            'screen': (
                '/static/css/admin.css',
            )
        }
        js = (
            '/static/js/jquery.undo.js',
            '/static/js/jquery.tablednd.js',
            '/static/js/admin-reorder.js',
            '/static/js/collapsed_stacked_inlines.js',
        )

    def queryset(self, request):
        return self.model.objects

    def get_urls(self):
        urls = super(SLBaseModelAdmin, self).get_urls()
        my_urls = patterns('',
            (move_regex, self.move),
        )
        return my_urls + urls

    def move(self, request, obj_id, direction):
        if not request.user.has_perm('%s.%s' % (self.model._meta.app_label,
                                                self.model._meta.get_change_permission())):
            raise Unauthorized

        obj = self.get_object(request, obj_id)
        if direction == 'up':
            obj.move_up()
        else:
            obj.move_down()

        return HttpResponseRedirect('../../../')

    def formfield_for_dbfield(self, db_field, **kwargs):
        if isinstance(db_field, models.DateTimeField):
            #raise Exception, db_field
            #kwargs['widget'] = AdminReadOnlyDateTimeWidget
            #kwargs['format'] = '%Y-%m-%d %H:%M:%S'
            pass

        #from django.db import models
        #from sorl.thumbnail.fields import ImageWithThumbnailsField
        #if (isinstance(db_field, ImageWithThumbnailsField) or isinstance(db_field, models.ImageField)):
        #    kwargs['widget'] = AdminImageWidget
        return super(SLBaseModelAdmin, self).formfield_for_dbfield(db_field, **kwargs)

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = list(self.readonly_fields)
        if issubclass(self.model, TimestampedModel):
            readonly_fields += ['created', 'modified']
        return readonly_fields

    def format_date(self, obj):
        return obj.date.strftime('%d %b %Y %H:%M')
    format_date.short_description = 'Date'

    def nice_created_date(self, obj):
        return obj.created.strftime('%d %b %Y %H:%M')
    nice_created_date.short_description = 'Date'

    def _related_link(self, target):
        return u'<a href="../../%s/%s/%s">%s</a>' % (
            target._meta.app_label,
            target._meta.module_name,
            target._get_pk_val(),
            unicode(target)
        )

class SLInlineModelAdmin(admin.options.InlineModelAdmin):
    """
    An inline model admin superclass
    """
    form = SLBaseModelForm

    def formfield_for_dbfield(self, db_field, **kwargs):
        from django.db import models
        #from sorl.thumbnail.fields import ImageWithThumbnailsField
        #if (isinstance(db_field, ImageWithThumbnailsField) or isinstance(db_field, models.ImageField)):
        #    kwargs['widget'] = AdminImageWidget
        return super(SLInlineModelAdmin, self).formfield_for_dbfield(db_field, **kwargs)

class SLStackedInline(SLInlineModelAdmin):
    template = 'admin/edit_inline/stacked.html'

class SLTabularInline(SLInlineModelAdmin):
    template = 'admin/edit_inline/tabular.html'
