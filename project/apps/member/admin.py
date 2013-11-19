from django.contrib import admin
from django.conf import settings
from django.core import urlresolvers
from django.http import HttpResponseRedirect
from django.utils.encoding import force_unicode
from django.utils.translation import ugettext as _
from django.db.models import Q

from sorl.thumbnail import default
ADMIN_THUMBS_SIZE = '60x60'
from sorl.thumbnail.admin import AdminImageMixin


from member.models import *
from xauto_lib.calutil import convDateAsFormat, convDatetimeToIsoDate
from multiuploader.models import MultiuploaderImage
from livesettings import models

from keywords.models import *
from xauto_lib.admin import SLBaseModelAdmin, SLStackedInline, SLTabularInline


class CityAdmin(SLBaseModelAdmin):
    """
    admin  for City database

    loc_id = models.BigIntegerField(default=0, db_index=True)
    country = models.CharField(max_length=2, null=True, blank=True)  # country code
    region = models.CharField(max_length=2, null=True, blank=True)  # choices=MESSAGE_TYPE
    city = models.CharField(max_length=255, null=True, blank=True)  # choices=MESSAGE_TYPE
    postal_code = models.CharField(max_length=6, null=True, blank=True)  # choices=MESSAGE_TYPE
    latitude = models.FloatField(default=0.00)
    longitude = models.FloatField(default=0.00)
    metro_code = models.IntegerField(default=0)
    area_code = models.CharField(max_length=3, null=True, blank=True)  # choices=MESSAGE_TYPE

    """
    list_display =  ('loc_id', 'country', 'region', 'city', 'postal_code',)
    list_filter = ('country',)
    search_fields = ('city', 'country',)
    fields = ('loc_id', 'country', 'region', 'city', 'postal_code', 'latitude', 'longitude', 'metro_code', 'area_code',)
    ordering = ('country', 'region' ,'city',)

class CityBlockAdmin(SLBaseModelAdmin):
    """
    admin  for City Block Ip range database

    begin_ip_num  = models.BigIntegerField(default=0, db_index=True)
    end_ip_num  = models.BigIntegerField(default=0, db_index=True)
    local = models.ForeignKey(GeoLiteCityLocation, related_name="city_location", null=True, blank=True)
    objects = GeoLiteCityBlockManager()

    """
    list_display =  ('begin_ip_num', 'end_ip_num', 'local',)
    search_fields = ('local',)
    fields = ('begin_ip_num', 'end_ip_num', 'local',)
    ordering = ('local',)


class CountryBlockIpRangeAdmin(SLBaseModelAdmin):
    """
    admin  for Country  Block Ip range database

    start_ip = models.CharField(max_length=20, null=True, blank=True, db_index=True)  # start ip
    end_ip = models.CharField(max_length=20, null=True, blank=True)  # end IP
    begin_ip_num  = models.BigIntegerField(default=0, db_index=True)
    end_ip_num  = models.BigIntegerField(default=0, db_index=True)
    country_code = models.CharField(max_length=4, null=True, blank=True, db_index=True)  # country code
    country = models.CharField(max_length=50, null=True, blank=True, db_index=True)  # country label

    """
    list_display =  ('start_ip', 'end_ip', 'begin_ip_num', 'end_ip_num', 'country_code', 'country',)
    search_fields = ('country_code', 'country', )
    fields = ('start_ip', 'end_ip', 'begin_ip_num', 'end_ip_num', 'country_code', 'country',)
    ordering = ('country_code',)


class MessageThreadAdmin(SLBaseModelAdmin):
    """
    admin  for Messages  Threads
    sender = models.ForeignKey(User, related_name='sent_messages_thread', null=True, blank=True)
    recipient = models.ForeignKey(User, related_name='received_messages_thread', null=True, blank=True)
    sent_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True)
    respond_at = models.DateTimeField(null=True, blank=True)
    sequence = models.IntegerField(default=1)
    status_thread = models.CharField(choices=STATUS_CHOICES, max_length=30, default='new', db_index=True)
    message = models.TextField()

    """
    list_display =  ('sender', 'recipient', 'sequence', 'status_thread', 'sent_at', 'respond_at')
    list_filter = ('status_thread', )
    search_fields = ('sender__email', 'status_thread', )
    fields = ('sender', 'recipient',  'status_thread', 'sequence', 'message',)
    ordering = ('status_thread', 'sender')
    readonly_fields = ("sent_at", "read_at", "respond_at", )


class MessageAdmin(SLBaseModelAdmin):
    """
    """
    list_display =  ('sender', 'type', 'read', 'recipient', 'event', 'subject', 'sent_at')
    list_filter = ('type', 'status')
    search_fields = ('sender__email', 'recipient__email', 'status', 'type')
    fields = ('read', 'sender', 'recipient',  'type' , 'chain_start',  'subject', 'message' , 'threads', 'status', 'removed_by', 'email', 'deleted', 'archived',)
    ordering = ('status', 'type' ,'sender')
    readonly_fields = ("sent_at", "read_at",)
    filter_horizontal = ('threads',)



class StatisticsAdmin(SLBaseModelAdmin):
    """
    """
    list_display =  ('event_stat', 'type_stat', 'target_stat', 'count_stat', 'content_type', 'object_id', )
    list_filter = ('event_stat', 'type_stat', 'target_stat', )
    search_fields = ('event_stat', 'type_stat')
    fields = ('event_stat', 'type_stat', 'target_stat', 'count_stat', 'content_type', 'object_id', 'country')
    ordering = ('event_stat', 'type_stat' ,'-count_stat')


class UserProfileAdmin(admin.ModelAdmin):
    """
    """

    list_display = ('getEmail', 'Follow', 'getuserName', 'created', 'ip_location', 'city', 'country', 'stdKey', 'media_mode', 'currency', 'avg_ratings', 'Language', 'is_deleted', 'is_suspended' ,'is_closed',)
    search_fields = ['name', 'city', 'country', 'about', 'user__first_name', 'user__last_name', 'user__email',]
    ordering = ('name', 'city' , 'country')
    list_per_page = 30
    filter_horizontal = ('keywords', 'comments', 'events',)
    list_filter = ['is_suspended', 'is_deleted' , 'country', 'is_organizer', 'is_attendee', 'is_closed']
    change_list_filter_template = "admin/filter_listing.html"

    def queryset(self, request):
        query = Q()
        qs = qs = self.model._default_manager.exclude(Q(name='') | Q(language=None))
        ordering = self.ordering or () # otherwise we might try to *None, which is bad ;)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs

    def getuserName(self, obj):
        return '%s-%s' % (obj.user.first_name, obj.user.last_name)

    def getEmail(self, obj):
        return '%s' % (obj.user.email)

    def Language(self, obj):
        return '%s' % (obj.language.language)

    def stdKey(self, obj):
        return '%s' % len(obj.keywords.all())


    def Follow(self, obj):
        nbrEventFollowing = obj.events.all()
        return '%s' % len(nbrEventFollowing)


class dupEmailAdmin(admin.ModelAdmin):
    """
    """
    list_display = ('subject', 'recipient', 'sent_at', 'sending_day',)
    search_fields = ['subject']
    list_filter = ['sending_day']
    ordering = ('-sent_at', )
    list_per_page = 30


class languageAdmin(admin.ModelAdmin):
    """
    addmin for language
    code = models.CharField(max_length=50, null=True, blank=True, db_index=True)
    language = models.CharField(max_length=50, null=True, blank=True, db_index=True)
    description = models.CharField(max_length=255, null=True, blank=True)

    """
    list_display = ('code', 'language', 'description',)
    search_fields = ['code']
    list_filter = ['code']
    ordering = ('code', )


class CommentUserAdmin(admin.ModelAdmin):

    list_display = ('author', 'comment',  'send_at',)
    search_fields = ['author']
    readonly_fields = ['send_at']
    list_filter = ['send_at']
    date_hierarchy = 'send_at'
    ordering = ('-send_at', 'author',)
    list_per_page = 30

admin.site.register(RecoveryQuestion)
admin.site.register(duplicateEmails, dupEmailAdmin)
admin.site.register(HelpQuestions)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Statistics, StatisticsAdmin)
admin.site.register(GeoLiteCityLocation, CityAdmin)
admin.site.register(GeoLiteCityBlock, CityBlockAdmin)
admin.site.register(GeoLiteCountryBlock, CountryBlockIpRangeAdmin)
admin.site.register(userLanguage, languageAdmin)
admin.site.register(MessageThread, MessageThreadAdmin)
admin.site.register(Message, MessageAdmin)


