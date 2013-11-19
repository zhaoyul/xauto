from django.contrib import admin
from django.db.models import Q

from sorl.thumbnail import default
ADMIN_THUMBS_SIZE = '60x60'
from sorl.thumbnail.admin import AdminImageMixin


from event.models import *
from member.models import *
#from cities_light.models import *
from xauto_lib.calutil import convDateAsFormat
from multiuploader.models import MultiuploaderImage
from flexselect import FlexSelectWidget

from keywords.models import *
from event.forms import *
from xauto_lib.admin import SLBaseModelAdmin, SLTabularInline


class MultiuploaderImageInline(admin.TabularInline):
    """
    userprofile = models.ForeignKey(UserProfile, blank=True, null=True, related_name='profile_images')
    event = models.ForeignKey(Event, blank=True, null=True, related_name='event_upload_images')
    filename = models.CharField(max_length=60, blank=True, null=True)
    key_data = models.CharField(max_length=90, unique=True, blank=True, null=True)
    image_type = models.CharField(max_length=10, blank=True, null=True)
    size = models.FloatField(default=0.0)
    upload_date = models.DateTimeField(auto_now_add=True)
    application = models.CharField(choices=IMAGE_TYPE, max_length=30, default='team')
    image = ResizedImageFieldWithThumbnail(max_width=800, max_height=600,  upload_to=storage,
    """

    extra = 0
    model = MultiuploaderImage
    search_fields = ["filename", "key_data", "application"]
    fields = ('filename', 'image_type', 'application', 'image', )
    list_display = [ "my_image_thumb", "filename", "image", "application", "userprofile", "event"]

    def my_image_thumb(self, obj):
        if obj.image:
            thumb = default.backend.get_thumbnail(obj.image.file, ADMIN_THUMBS_SIZE)
            return u'<img width="%s" src="%s" />' % (thumb.width, thumb.url)
        else:
            return "No Image"
        my_image_thumb.short_description = 'My Thumbnail'
        my_image_thumb.allow_tags = True



class EventImageExtendInline(AdminImageMixin, admin.ModelAdmin):
    model = EventImageExtend
    extra = 1
    fields = ('image', 'caption', 'created', 'modified', 'order')

class YoutubeVideoIdAdmin(admin.ModelAdmin):
    class Media:
        js = ('lib/youtube/swfobject.js',
            'js/youtube_admin_preview.js',)

class YoutubeVideoIdInline( admin.TabularInline):
    model = YoutubeVideoId
    fk_name = "event"


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



class FeedBackInline(SLTabularInline):
    """
    """

    model = Feedback
    extra = 0
    fields = ('comment', 'event', 'created', 'modified', )
    readonly_fields = ("send_at",)


class FeedBackRatingValueInline(admin.TabularInline):
    """
    rate_type = models.ForeignKey(RatingValue)
    feedback = models.ForeignKey(Feedback, related_name='rating')
    rating = models.FloatField()
    """

    model = RatingValue
    extra = 0
    fields = ('name', )


class FeedBackRatingInline(admin.TabularInline):
    """
    rate_type = models.ForeignKey(RatingValue)
    rating = models.FloatField()
    """

    inlines = [
        FeedBackRatingValueInline,
        ]
    model = FeedbackRating
    extra = 0
    fields = ('rate_type', 'rating', 'author', 'created', 'modified', )
    sortable_field_name = "rate_type"



class FeedBackAdmin(SLBaseModelAdmin):
    """
    """

    model = Feedback
    fields = ('author' ,'given_author', 'comment', 'event', 'created', 'modified', 'rating', 'recommend',)
    readonly_fields = ("send_at",)
    list_display = ('author', 'given_author', 'event', 'comment', 'send_at', 'getAuthorEvent' , 'avgRatings',)
    filter_horizontal = ('rating',)
    search_fields = ['comment', 'event__title', 'author__email', ]

    def getRating(self, obj):
        return ''

    def getAuthorEvent(self, obj):
        return '%s' % (obj.event.author)

    def avgRatings(self, obj):
        avgRating = obj.getAvgFeedback
        return avgRating


class FeedBackRatingAdmin(SLBaseModelAdmin):
    """
    ----- ratings ---
    """

    model = FeedbackRating
    fields = ('author', 'event', 'rate_type', 'rating',  'created', 'modified', )
    list_display = ('author', 'event', 'created', 'rating', 'rate_type',)
    list_filter = ['rating', ]
    ordering = ('event',)

class EventDateInline(admin.TabularInline):
    """
    Inline admin  for Event Date
    """
    model = EventDate
    extra = 0
    fields = ( 'author', 'start_date', 'end_date', 'feature_headline', 'attend_free', 'exhibit_free', )



class UserProfileInline(admin.TabularInline):
    """
    Inline admin  for User profile who are following specific events
    """
    model = UserProfile
    extra = 0
    fields = ( 'user', 'city', 'country',)





class EventOrganizerInline(admin.TabularInline):
    """
    Inline admin  for Event Organizer
    organization_name = models.CharField(max_length=255, default='')
    organization_desc = models.TextField(null=True, blank=True, default='')
    events = models.ManyToManyField('Event', related_name='event_for_user')
    venues = models.ManyToManyField('Venue', related_name='venue_for_user')
    author = models.ForeignKey(User, related_name='organizer_event', verbose_name='User Who Organize the Event')
    remove_past_events = models.BooleanField(default=False)
    is_saved = models.BooleanField(default=False)
    include_social_link = models.BooleanField(default=False)
    shortname = models.CharField(max_length=255, default='')
    facebook_id = models.CharField(max_length=255, default='')
    twitter_id = models.CharField(max_length=255, default='')

    """
    model = Organizer
    extra = 0
    fields = ( 'author', 'organization_name', 'organization_desc',  )





class EventVenueInline(admin.TabularInline):
    """
    Inline admin  for Event Venue
    organizer = models.ForeignKey(Organizer, related_name='organizer_venue', verbose_name='Event Organizer')
    user = models.ForeignKey(User, related_name='user_venue', verbose_name='User who create the Venue')
    venue = models.CharField(max_length=255)
    address = models.CharField(max_length=255, default='', null=True, blank=True)
    address_2 = models.CharField(max_length=255, default='', null=True, blank=True)
    country = models.ForeignKey('cities_light.Country', null=True, blank=True, related_name='venue_country', verbose_name='Country Code')
    city = models.CharField(max_length=255,null=True, blank=True)
    state = models.CharField(max_length=255,null=True, blank=True)
    region = models.CharField(max_length=255,null=True, blank=True)
    zipcode = models.CharField(max_length=255, null=True, blank=True)
    latitude = models.FloatField(default=0.00)
    longitude = models.FloatField(default=0.00)
    longaddress = models.CharField(max_length=255)
    zoom = models.FloatField(default=0.00)
    is_saved = models.BooleanField(default=False)

    """
    model = Venue
    extra = 0
    fields = ( 'venue', 'address', 'zipcode', 'city',  'state', 'country',)


class EventAdminInline(SLTabularInline):
    """
    title = models.CharField(max_length=255)
    description = models.TextField()
    keywords = models.ManyToManyField(KeywordService, related_name='user_keywords', null=True, blank=True)
    available_dates = models.ManyToManyField('EventDate', related_name='select_event_date', null=True, blank=True)
    author = models.ForeignKey(User, related_name='authored_event')
    """

    model = Event
    fields = ('title', 'author', 'venue', 'organizer', )
    list_display = ('title', 'author', 'created', )
    ordering = ('title',)
    extra = 0


class EventAdmin(AdminImageMixin, admin.ModelAdmin):
    """
    Main Event Admin tool
    title = models.CharField(max_length=255)
    description = models.TextField()
    keywords = models.ManyToManyField(KeywordService, related_name='user_keywords')
    available_dates = models.ManyToManyField('EventDate', related_name='select_event_date')

    author = models.ForeignKey(User, related_name='authored_event')
    profile = models.ForeignKey('member.UserProfile', related_name='event_user_profile', null=True, blank=True)
    published_at = models.DateTimeField(auto_now_add=True)
    expire_at = models.DateTimeField(null=True)
    duration = models.PositiveIntegerField(default=0)

    number = models.CharField(max_length=20, db_index=True, blank=True, null=True)
    status = models.CharField(max_length=15, db_index=True, choices=STATUS_CHOICES)
    eventSize = models.IntegerField(choices=EVENT_SIZE, default=10)  # How big is your event in Cars
    capacity = models.IntegerField(default=0)  # How big is your Capacity in people in people

    started_at = models.DateTimeField(null=True, blank=True)
    closed_at = models.DateTimeField(null=True, blank=True)
    archived_at = models.DateTimeField(null=True, blank=True)

    objects = DistanceManager()
    objtimes = DateDiffManager()
    main_image = models.ForeignKey('EventImageExtend', on_delete=models.SET_NULL, blank=True, null=True, related_name='main')
    video_cache = models.CharField(default='[]', max_length=255)
    youtube_url = YouTubeField(blank=True)
    video_url = models.URLField(null=True, blank=True)

    active = manager_from(EventManagerMixin, queryset_cls=ActiveEventQuerySet)   # -- pre-List Active Events ---
    valids = manager_from(EventManagerMixin, queryset_cls=EventQuerySet)

    google_analytics = models.CharField(default='', max_length=50)
    instructions = models.CharField(default='', max_length=250)


    """
    save_on_top = True


    #formfield_overrides = {
    #        models.CharField: {'widget': TextInput(attrs={'width':'400'})},
    #        models.TextField: {'widget': Textarea(attrs={'rows':4, 'cols':120})},
    #    }


    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.8/jquery-ui.min.js',
            'http://code.jquery.com/jquery-1.4.2.min.js',
            'http://maps.google.com/maps/api/js?sensor=true',
            '/static/lib/json2.js',
            '/static/lib/tools/jquery.tools.min.js',
            '/static/js/xauto/base_code.min.js',
            '/static/js/xauto/gmaps_admin.js',
            '/static/js/xauto/geo_autocomplete.js',
            '/static/js/xauto/admin_display_thumbs.js',
            '/static/lib/youtube/swfobject.js',
            '/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
            '/static/grappelli/tinymce_setup/tinymce_setup.js',
            '/static/js/xauto/youtube_admin_preview.js',
        )
        css = {
            'all' : ('/static/css/xauto_admin.css',)
            }


    inlines = [
        EventDateInline,
        MultiuploaderImageInline,
        ]

    fieldsets = (
        ('General', {
            'fields': ('number', 'title', 'description', 'duration', 'author', 'venue', 'Event_Location', 'organizer', ),
            }),
        ('Follow, Tags and Dates', {
            'classes' : ('grp-collapse grp-open',),
            'fields'  : ('keywords', 'event_date', 'followed',),
            }),
        ('Details', {
            'classes' : ('grp-collapse grp-open',),
            'fields'  : ('status', 'eventSize', 'capacity', 'shortname',),
            }),
        ('Date', {
            'classes' : ('grp-collapse grp-open',),
            'fields'  : ('started_at', 'closed_at', 'archived_at', 'published_at', 'expire_at', ),
            }),
        )

    readonly_fields = ("published_at", "Event_Location", )
    list_display = ('title', 'number', 'Author', 'EVENT_IMAGE', 'FollowedBy', 'Posted',  'Expire', 'Organize', 'Area', 'NbrDates', )
    search_fields = ['title', 'author__email', 'status', ]
    list_filter = ['status',  'duration', ]
    date_hierarchy = 'published_at'
    ordering = ('-published_at', 'number', 'author', )
    filter_horizontal = ('keywords', 'event_date', 'followed',)
    change_list_filter_template = "admin/filter_listing.html"
    autocomplete_lookup_fields = {
        'title': ['title'],
        }

    def Event_Location(self, instance):
        objEvent = self
        objEvent2 = instance
        formattedAddress = objEvent2.getShortLocation(mode='formatted')
        return formattedAddress

    Event_Location.short_description = "Event Address"
    Event_Location.allow_tags = True

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        object_id = request.META['PATH_INFO'].strip('/').split('/')[-1]
        if db_field.name == 'organizer':
            if CheckNumeric(object_id):
                currentInstance = Event.objects.get(pk=object_id)
                kwargs['queryset'] = Organizer.objects.filter(author=currentInstance.author)
            else:
                kwargs['widget'] =  displayOrganizerWidget(
                    base_field=db_field,
                    modeladmin=self,
                    request=request,
                 )
                kwargs['label'] = 'Available Organizer(s)'
        elif db_field.name == 'venue':
            if CheckNumeric(object_id):
                currentInstance = Event.objects.get(pk=object_id)
                kwargs['queryset'] = Venue.objects.filter(user=currentInstance.author)
            else:
                kwargs['widget'] =  displayVenueWidget(
                    base_field=db_field,
                    modeladmin=self,
                    request=request,
                 )
                kwargs['label'] = 'Available Venue(s)'


        return super(EventAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        object_id = request.META['PATH_INFO'].strip('/').split('/')[-1]
        if db_field.name == 'event_date':
            if CheckNumeric(object_id):
                currentInstance = Event.objects.get(pk=object_id)
                kwargs['queryset'] = EventDate.objects.filter(event=currentInstance)
            else:
                kwargs['queryset'] = EventDate.objects.filter(event__isnull=True)
        elif db_field.name == 'keywords':
            currentInstance = MainKeywordService.objects.get(name='Autos & Crafts')
            kwargs['queryset'] = KeywordService.objects.filter(parent=currentInstance)
        return super(EventAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)



    def Keyword(self, obj):
        return '%s' % len(obj.keywords.all())

    def NbrDates(self, obj):
        nbrDates = obj.event_date.all()
        return len(nbrDates)

    def Organize(self, obj):
        if obj.organizer:
            return '%s' % obj.organizer.shortname

    def Area(self, obj):
        if obj.venue:
            return '%s, %s' % (obj.venue.city, obj.venue.country_short)


    def queryset(self, request):
        query = Q()
        qs = qs = self.model._default_manager.exclude(Q(status__in=['draft', '']) | Q(title='*'))
        ordering = self.ordering or () # otherwise we might try to *None, which is bad ;)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs

    def Posted(self, obj):
        return '%s' % (convDateAsFormat(obj.published_at, '%Y-%m-%d %H:%M:%S', '%Y-%m-%d'))

    def Expire(self, obj):
        return '%s' % (convDateAsFormat(obj.expire_at, '%Y-%m-%d %H:%M:%S', '%Y-%m-%d'))

    def Author(self, obj):
        return '%s' % (obj.author.email)

    def FollowedBy(self, obj):
        return '%s' % (obj.followed.all().count())

class displayVenueWidget(FlexSelectWidget):
    trigger_fields = ['author']
    def details(self, base_field_instance, instance):
        return ""
    def queryset(self, instance):
        author = instance.author
        return Venue.objects.filter(user=author)
    def empty_choices_text(self, instance):
        return "Please Create New Venue"

class displayOrganizerWidget(FlexSelectWidget):
    trigger_fields = ['author']
    def details(self, base_field_instance, instance):
        return ""
    def queryset(self, instance):
        author = instance.author
        return Organizer.objects.filter(author=author)
    def empty_choices_text(self, instance):
        return "Please Create New Organizer"


class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('country', 'currency',)
    search_fields = ['country', 'currency']
    readonly_fields = ['country']
    ordering = ('country',)


class flagEventAdmin(admin.ModelAdmin):
    """
    """

    list_display = ('reason', 'Event', 'Author', 'created', 'review', 'remove_event', 'email_sent', 'NbrMsg')
    list_filter = ('review' , 'remove_event',  'email_sent', )
    fields = ('event', 'author', 'reason', 'description', 'response', 'active', 'email_sent', 'message_sent', 'review', 'remove_event', 'date_email', 'date_review', 'answers',)
    ordering = ('-created',)
    filter_horizontal = ('answers',)

    def Event(self, obj):
        return '%s' % obj.event.title

    def Author(self, obj):
        return '%s' % event.author.email

    def NbrMsg(self, obj):
        return '%s' % len(obj.answers.all())

    def get_object_spec(self, request, model):
            object_id = request.META['PATH_INFO'].strip('/').split('/')[-1]
            try:
                object_id = int(object_id)
                return model.objects.get(pk=object_id)
            except:
                return None

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        """
        Alters the widget displayed for the base field.
        """
        if db_field.name == "answers":
            flagObject  = self.get_object_spec(request, flagEvent)
            if flagObject:
                kwargs['queryset'] = Message.objects.filter(event=flagObject.event, type=Message.FLAGEVENT)
                kwargs['label'] = 'Messages/Answers for this Event'
        return super(flagEventAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)



class StatisticsAdmin(SLBaseModelAdmin):
    """
    admin  for Statistics Model

    event_stat  = models.CharField(choices=STATISTIC_CHOICES, max_length=55, null=True, blank=True, default='search')
    type_stat  = models.CharField(choices=STATISTIC_OBJECT, max_length=55, null=True, blank=True, default='keyword')
    count_stat = models.IntegerField(default=0) # count access on this Object/event
    content_type = models.ForeignKey(ContentType, blank=True, null=True)
    object_id = models.PositiveIntegerField(blank=True, null=True)

    """
    list_display =  ('event_stat', 'type_stat', 'target_stat', 'count_stat', 'content_type', 'object_id', )
    list_filter = ('event_stat', 'type_stat', 'target_stat', )
    search_fields = ('event_stat', 'type_stat')
    fields = ('event_stat', 'type_stat', 'target_stat', 'count_stat', 'content_type', 'object_id', 'country')
    ordering = ('event_stat', 'type_stat' ,'-count_stat')


class CommentEventAdmin(admin.ModelAdmin):
    """
    addmin for comments
    """
    list_display = ('event', 'sent_direction', 'short_message', 'sent_at',)
    search_fields = ['event']
    list_filter = ['sent_at']
    date_hierarchy = 'sent_at'
    ordering = ('-sent_at', 'event',)
    list_per_page = 30
    form = MessageAdminForm


class dupEmailAdmin(admin.ModelAdmin):
    """
    """
    list_display = ('subject', 'recipient', 'sent_at', 'sending_day',)
    search_fields = ['subject']
    list_filter = ['sending_day']
    ordering = ('-sent_at', )
    list_per_page = 30



class EventDateAdmin(SLBaseModelAdmin):
    """
    event = models.ForeignKey('Event', related_name='event_date', verbose_name='Event Date')
    author = models.ForeignKey(User, related_name='user_event_date', verbose_name='Event Date')
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    feature_headline = models.CharField(max_length=255)
    feature_detail = models.TextField()
    currency = models.ForeignKey(Currency)
    attend_free = models.BooleanField(default=False)
    exhibit_free = models.BooleanField(default=False)
    attend_price_from = models.FloatField(default=0)  # price range from (attend)
    attend_price_to = models.FloatField(default=0)  # price range from (attend)
    exhibit_price_from = models.FloatField(default=0)  # price range from (exhibit)
    exhibit_price_to = models.FloatField(default=0)  # price range from (exhibit)

    """

    model = Feedback
    list_display = ('author' ,'eventTitle', 'start_date', 'end_date', 'created', 'modified', 'attend_free',)
    #readonly_fields = ("send_at",)
    fields = ('event', 'author', 'start_date', 'end_date', 'feature_headline', 'feature_detail', 'currency' , 'attend_free', 'attend_price_from', 'attend_price_to', 'exhibit_free',  'exhibit_price_from', 'exhibit_price_to', )
    search_fields = ['attend_free', 'exhibit_free', ]

    def eventTitle(self, obj):
        return '%s' % obj.event.title



class EventOrganizerAdmin(SLBaseModelAdmin):
    """
    organization_name = models.CharField(max_length=255, default='')
    organization_desc = models.TextField(null=True, blank=True, default='')
    events = models.ManyToManyField('Event', related_name='event_for_user')
    venues = models.ManyToManyField('Venue', related_name='venue_for_user')
    author = models.ForeignKey(User, related_name='organizer_event', verbose_name='User Who Organize the Event')
    remove_past_events = models.BooleanField(default=False)
    is_saved = models.BooleanField(default=False)
    include_social_link = models.BooleanField(default=False)
    shortname = models.CharField(max_length=255, default='')
    facebook_id = models.CharField(max_length=255, default='')
    twitter_id = models.CharField(max_length=255, default='')

    """

    inlines = [
        EventAdminInline,
        ]

    model = Feedback
    list_display = ('shortname', 'author' ,'organization_name', 'is_saved', 'include_social_link', 'created', 'NbrEvents',)
    fields = ('organization_name', 'organization_desc', 'events', 'venues', 'author', 'remove_past_events', 'is_saved' , 'include_social_link', 'shortname', 'facebook_id', 'twitter_id', )
    search_fields = ['is_saved', 'include_social_link', 'remove_past_events', ]
    list_filter = ['is_saved']
    date_hierarchy = 'created'
    ordering = ('-created', 'shortname',)
    list_per_page = 30
    filter_horizontal = ('events', 'venues',)

    def NbrEvents(self, obj):
        nbrEvent = Event.objects.filter(organizer=obj).count()
        return '%s' % nbrEvent



class EventVenueAdmin(SLBaseModelAdmin):
    """
    Venue admin tool
    """

    class Media:
        js = [
        'http://ajax.googleapis.com/ajax/libs/jqueryui/1.8/jquery-ui.min.js',
        'http://code.jquery.com/jquery-1.4.2.min.js',
        'http://maps.google.com/maps/api/js?sensor=true',
        '/static/lib/json2.js',
        '/static/lib/tools/jquery.tools.min.js',
        '/static/js/xauto/base_code.min.js',
        '/static/js/xauto/gmaps_admin.js',
        '/static/js/xauto/geo_autocomplete.js',
        ]
        css = {
            'all' : ('/static/css/xauto_admin.css',)
            }

    inlines = [
        EventAdminInline,
        ]


    model = Venue
    list_display = ('OrgName', 'venue', 'city' ,'country', 'is_saved',  'created', 'Creator', 'NbrEvents',)
    fields = ('organizer', 'user', 'venue', 'longaddress',  'address', 'address_2', 'country', 'country_short', 'city' , 'state', 'region', 'zipcode', 'latitude', 'longitude', 'zoom',  'is_saved',)
    search_fields = ['is_saved', 'country', ]
    list_filter = ['is_saved', 'country']
    date_hierarchy = 'created'
    ordering = ('-created', 'country',)
    list_per_page = 30

    def OrgName(self, obj):
        return '%s' % obj.organizer.shortname
    def Creator(self, obj):
        return '%s' % obj.user.email

    def NbrEvents(self, obj):
        nbrEvent = Event.objects.filter(venue=obj).count()
        return '%s' % nbrEvent

admin.site.register(Currency, CurrencyAdmin)
admin.site.register(Feedback, FeedBackAdmin)
admin.site.register(EventImageExtend, EventImageExtendInline)
admin.site.register(FeedbackRating, FeedBackRatingAdmin)
admin.site.register(RatingValue)
admin.site.register(Event, EventAdmin)
admin.site.register(flagEvent, flagEventAdmin)
admin.site.register(YoutubeVideoId, YoutubeVideoIdAdmin)
admin.site.register(EventDate, EventDateAdmin)
admin.site.register(Organizer, EventOrganizerAdmin)
admin.site.register(Venue, EventVenueAdmin)


