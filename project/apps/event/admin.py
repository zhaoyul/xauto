from django.contrib import admin
from django.db.models import Q

from sorl.thumbnail.admin import AdminImageMixin
from sorl.thumbnail import default
ADMIN_THUMBS_SIZE = '60x60'

from event.models import EventDate, Event, EventImage, Currency
from multiuploader.models import MultiuploaderImage


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
    list_display = [ "my_image_thumb", "filename", "image", "application", "userprofile", "event_date"]

    def my_image_thumb(self, obj):
        if obj.image:
            thumb = default.backend.get_thumbnail(obj.image.file, ADMIN_THUMBS_SIZE)
            return u'<img width="%s" src="%s" />' % (thumb.width, thumb.url)
        else:
            return "No Image"
        #my_image_thumb.short_description = 'My Thumbnail'
        #my_image_thumb.allow_tags = True


class EventImageInline(AdminImageMixin, admin.ModelAdmin):
    model = EventImage
    extra = 1
    fields = ('image', 'caption', 'created', 'modified')

class EventDateInline(admin.TabularInline):
    """
    Inline admin  for Event Date
    """
    model = EventDate
    extra = 0
    fields = ( 'location_name', 'start_date', 'end_date', 'feature_headline', 'attend_free', 'exhibit_free', )


class EventAdmin(AdminImageMixin, admin.ModelAdmin):
    """
    Main Event Admin tool
    title = models.CharField(max_length=255, null=True, blank=True)
    about = models.TextField()

    author = models.ForeignKey(User, related_name='authored_event', null=True, blank=True)
    profile = models.ForeignKey('member.UserProfile', related_name='event_user_profile', null=True, blank=True)
    duration = models.PositiveIntegerField(default=0, verbose_name='Duration in Days')

    status = models.CharField(max_length=15, db_index=True, choices=STATUS_CHOICES, default=STATUS_NEW)
    eventSize = models.IntegerField(choices=EVENT_SIZE, default=10)  # How big is your event in Cars
    capacity = models.IntegerField(default=0)  # How big is your Capacity in people in people
    short_link = models.CharField(max_length=50, default='')

    main_image = models.ForeignKey('EventImage', on_delete=models.SET_NULL, blank=True, null=True, related_name='main')
    video_cache = models.CharField(default='[]', max_length=255)

    followed = models.ManyToManyField('member.UserProfile', related_name='events', null=True, blank=True, verbose_name='Event followed by')
    """
    save_on_top = True


    inlines = [
        EventDateInline,
        ]

    fieldsets = (
        ('General', {
            'fields': ('title', 'about', 'author', 'main_image'),
            }),
        ('Followed', {
            'classes' : ('grp-collapse grp-open',),
            'fields'  : ('followed',),
            }),
        ('Details', {
            'classes' : ('grp-collapse grp-open',),
            'fields'  : ('status', 'eventSize', 'capacity', 'short_link',),
            }),
        )

    list_display = ('title', 'Author', 'main_image', )
    search_fields = ['title', 'author__email', 'status', ]
    list_filter = ['status', ]
    change_list_filter_template = "admin/filter_listing.html"
    autocomplete_lookup_fields = {
        'title': ['title'],
        }

    def queryset(self, request):
        qs = qs = self.model._default_manager.exclude(Q(status__in=['draft', '']) | Q(title='*'))
        ordering = self.ordering or () # otherwise we might try to *None, which is bad ;)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs

    def Author(self, obj):
        if obj.author:
            return '%s' % (obj.author.full_name)
        return ""


class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('country', 'currency',)
    search_fields = ['country', 'currency']
    #readonly_fields = ['country']
    ordering = ('country',)


class EventDateAdmin(admin.ModelAdmin):
    """
    location_name = models.CharField(max_length=250, default='', null=True, blank=True)
    latitude = models.FloatField(default=0.00)
    longitude = models.FloatField(default=0.00)
    address_1 = models.CharField(max_length=100, default='', null=True, blank=True)
    address_2 = models.CharField(max_length=100, default='', null=True, blank=True)
    country = models.CharField(max_length=50,null=True, blank=True)
    country_short = models.CharField(max_length=50,null=True, blank=True)
    city = models.CharField(max_length=100,null=True, blank=True)
    state = models.CharField(max_length=50,null=True, blank=True)
    region = models.CharField(max_length=50,null=True, blank=True)
    zipcode = models.CharField(max_length=20, null=True, blank=True)
    event = models.ForeignKey('Event', related_name='event_available_date', verbose_name='Your Event')
    author = models.ForeignKey(User, related_name='user_event_date', verbose_name='Event Author')
    start_date = models.DateTimeField(null=True, blank=False)
    end_date = models.DateTimeField(null=True, blank=True)
    feature_headline = models.CharField(max_length=100)
    feature_detail = models.TextField()
    currency = models.ForeignKey(Currency, null=True, blank=True ) #, default=lambda: Currency.objects.get(currency='USD', country_code='US')
    attend_free = models.BooleanField(default=False)
    exhibit_free = models.BooleanField(default=False)
    attend_price_from = models.FloatField(default=0.0, verbose_name='Attend Price US$ (From)')    # price range from (attend)
    attend_price_to = models.FloatField(default=0.0, verbose_name='Attend Price US$ (To)')      # price range from (attend)
    exhibit_price_from = models.FloatField(default=0.0, verbose_name='Exhibit Price US$ (From)')   # price range from (exhibit)
    exhibit_price_to = models.FloatField(default=0.0, verbose_name='Exhibit Price US$ (To)')     # price range from (exhibit)

    """
    inlines = [
        MultiuploaderImageInline,
        ]
    list_display = ('location_name', 'start_date', 'end_date', 'created', 'modified', 'attend_free',)
    #readonly_fields = ("send_at",)
    fields = ('event', 'location_name', 'address_1', 'address_2', 'country', 'country_short', 'city' , 'state', 'region', 'zipcode', 'latitude', 'longitude', 'start_date', 'end_date', 'feature_headline', 'feature_detail', 'currency' , 'attend_free', 'attend_price_from', 'attend_price_to', 'exhibit_free',  'exhibit_price_from', 'exhibit_price_to', )
    search_fields = ['attend_free', 'exhibit_free', ]

    def eventTitle(self, obj):
        return '%s' % obj.event.title

admin.site.register(Currency, CurrencyAdmin)
admin.site.register(EventImage, EventImageInline)
admin.site.register(Event, EventAdmin)
admin.site.register(EventDate, EventDateAdmin)


