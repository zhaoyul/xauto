from django.contrib import admin
from account.models import AlertEvent, AlertSystem, AlertSent, Parameters, Application


class AlertEventAdmin(admin.ModelAdmin):
    """
    """

    list_display = ('user', 'type','frequency',  'status', 'last_sent_at', 'nbr_sent', 'nbr_alert',)
    list_filter = ('status', 'type', 'activated', )
    search_fields = ('keywords', 'category')
    fields = ('user', 'event', 'type', 'distance', 'frequency', 'location_address', 'latitude', 'longitude', 'activated',  'status', 'keywords', 'user_keywords', 'nbr_sent', 'nbr_alert',)
    ordering = ('-created', 'keywords', 'type' ,'status')
    filter_horizontal = ('keywords',  'user_keywords')


class AlertSystemAdmin(admin.ModelAdmin):
    """
    """

    list_display = ('user', 'new_message_received',  )
    search_fields = ('user', 'category')
    fields = ('user', 'signup', 'activation', 'password_recovery',
              'new_message_received', 'frequency_attendee',
              'nbr_alert', 'nbr_email',
              )
    ordering = ('user', )
    readonly_fields = ("last_sent_email", )


class AlertEventSentAdmin(admin.ModelAdmin):
    """
    """

    list_display = ( 'event', 'alert', 'frequency',  'sent_at' , 'type_alert',)
    fields = ( 'frequency', 'event', 'message', 'alert', 'type_alert',)



class ApplicationAdmin(admin.ModelAdmin):
    """
    application = models.ForeignKey(Application, verbose_name=_('Django Application'))
    group = models.CharField(max_length=100, blank=False, null=False)
    """

    list_display = ('application', 'description', )
    fields = ('application', 'description', )
    ordering = ('application', )


class ParameterAdmin(admin.ModelAdmin):
    """
    application = models.ForeignKey(Application, verbose_name=_('Django Application'))
    group = models.CharField(max_length=100, blank=False, null=False)
    key = models.CharField(max_length=100, blank=False, null=False)
    value = models.CharField(max_length=255, blank=True)
    sequence = models.IntegerField(default=1)
    array = models.BooleanField(default=False)
    """

    class Media:
        js = (
            '/static/js/xauto/admin_display_thumbs.js',
            '/static/lib/youtube/swfobject.js',
            '/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
            '/static/grappelli/tinymce_setup/tinymce_setup.js',
        )

    list_display = ('application','group',  'key', 'value', 'label', 'sequence', 'array', 'staticpage' , 'flatpage', 'enable')
    search_fields = ('key', 'value')
    fields = ('application','group',  'key', 'label', 'value', 'sequence', 'array', 'flatpage', 'staticpage', 'enable', 'help', 'title', 'description', 'url_href',)
    ordering = ('application', 'group', 'key', 'value',)
    list_filter = ('application', 'group', 'key', 'flatpage', 'staticpage',)

admin.site.register(AlertSent, AlertEventSentAdmin)
admin.site.register(AlertEvent, AlertEventAdmin)
admin.site.register(AlertSystem, AlertSystemAdmin)
admin.site.register(Parameters, ParameterAdmin)
admin.site.register(Application, ApplicationAdmin)

