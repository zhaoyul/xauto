# ---------------------------------------------------
# --- Django base core code (system)              ---
from django.db import models
from django.db.models import permalink
from django.core.exceptions import ValidationError

# ---------------------------------------------------
# --- Django addon                                ---
from django.utils import timezone
from sorl.thumbnail.fields import ImageField
from autoslug import AutoSlugField
from sorl.thumbnail import get_thumbnail
from django_countries.fields import CountryField
from account.models import UserProfile
from xauto_lib.models import TimestampedModel
from multiuploader.models import MultiuploaderImage
from timezone_field import TimeZoneField


class Currency(models.Model):
    currency = models.CharField(max_length=5)
    symbol = models.CharField(max_length=40, null=True)

    class Meta:
        verbose_name_plural = 'Currencies'

    def __unicode__(self):
        return u'{}'.format(self.currency)

    def get_currency(self):
        return self.symbol if self.symbol else ''
    currency_symbol = property(get_currency)

    def get_currency_name(self):
        return self.currency
    currency_name = property(get_currency_name)

    def get_symbol(self):
        return self.symbol if self.symbol else ''


class EventDate(TimestampedModel):
    """
    Django models in relation with Event Models (Event Date)
    Start / End Date  - Price/Cost / featured
    """
    event = models.ForeignKey('Event', related_name='event_dates',
                              verbose_name='Your Event')
    location_name = models.CharField(max_length=250, default='', null=True, blank=True)
    latitude = models.FloatField(default=0.00)
    longitude = models.FloatField(default=0.00)
    address_1 = models.CharField(max_length=100, default='', null=True, blank=True)
    address_2 = models.CharField(max_length=100, default='', null=True, blank=True)
    country = CountryField(null=True, blank=True)
    city = models.CharField(max_length=100,null=True, blank=True)
    state = models.CharField(max_length=50,null=True, blank=True)
    region = models.CharField(max_length=50,null=True, blank=True)
    zipcode = models.CharField(max_length=20, null=True, blank=True)

    timezone = TimeZoneField(null=False, blank=False, default='UTC')
    start_date = models.DateTimeField(null=True, blank=False)
    end_date = models.DateTimeField(null=True, blank=True)
    feature_headline = models.CharField(max_length=100)
    feature_detail = models.TextField()
    currency = models.ForeignKey(Currency, null=True, blank=True)
    attend_free = models.BooleanField(default=False)
    exhibit_free = models.BooleanField(default=False)
    attend_price_from = models.FloatField(default=0.0,
        verbose_name='Attend Price US$ (From)')    # price range from (attend)
    attend_price_to = models.FloatField(default=0.0,
        verbose_name='Attend Price US$ (To)')      # price range from (attend)
    exhibit_price_from = models.FloatField(default=0.0,
        verbose_name='Exhibit Price US$ (From)')   # price range from (exhibit)
    exhibit_price_to = models.FloatField(default=0.0,
        verbose_name='Exhibit Price US$ (To)')     # price range from (exhibit)
    shared = models.ManyToManyField(UserProfile, null=True, blank=True,
                                    related_name='shared_dates')

    class Meta:
        ordering = ('-start_date',)

    def __unicode__(self):
        return '(%s) - %s/%s' % (self.event.title.capitalize(),
                                 self.start_date, self.end_date)


class Event(TimestampedModel):
    STATUS_NEW = 'new'
    STATUS_CANCELED = 'canceled'
    STATUS_REMOVED = 'removed'
    STATUS_CLOSED = 'closed'
    STATUS_EXPIRED = 'expired'
    STATUS_DRAFT = 'draft'
    STATUS_ARCHIVED = 'archived'
    STATUS_PENDING = 'pending'
    STATUS_COMPLETE = 'completed',

    STATUS_CHOICES = (
        (STATUS_NEW, 'New'),
        (STATUS_DRAFT, 'Draft',),
        (STATUS_COMPLETE, 'Completed'),
        (STATUS_CANCELED, 'Canceled'),
        (STATUS_CLOSED, 'Closed'),
        (STATUS_REMOVED, 'Removed'),
        (STATUS_EXPIRED, 'Expired'),
        (STATUS_ARCHIVED, 'Archived'),
        (STATUS_PENDING, 'Event in pending Status'),
    )

    EVENT_SIZE = (
        (10, '10 Cars'),
        (25, '25 Cars',),
        (50, '50 Cars'),
        (100, '100 Cars'),
        (150, '150+ Cars'),
    )

    SORT_CHOICES = {
        'Show Last Event':  '-created',
        'endingtime':  'expire_at',
        'dateposted':  'published_at',
        'distance':  'distance',
        '-endingtime':  '-expire_at',
        '-dateposted':  '-published_at',
        '-distance':  'published_at',
        }

    STATUS_COMPLETED_EVENT = [STATUS_COMPLETE, ]

    title = models.CharField(max_length=255, null=True, blank=True)
    about = models.TextField()

    author = models.ForeignKey(UserProfile, related_name='authored_event',
        null=True, blank=True)

    duration = models.PositiveIntegerField(default=0,
         verbose_name='Duration in Days')

    status = models.CharField(max_length=15, db_index=True,
        choices=STATUS_CHOICES, default=STATUS_NEW)
    eventSize = models.IntegerField(choices=EVENT_SIZE, default=10)  # How big is your event in Cars
    capacity = models.IntegerField(default=0)  # How big is your Capacity in people in people

    short_link = models.CharField(max_length=50, default='', unique=True)

    slug = AutoSlugField(populate_from='short_link',
        slugify=lambda value: value.replace(' ', '-'),
        always_update=True,
        unique=True)

    main_image = models.ForeignKey('EventImage', on_delete=models.SET_NULL,
        blank=True, null=True, related_name='main')

    followed = models.ManyToManyField(UserProfile,
        related_name='followed_events', null=True, blank=True,
        verbose_name='Event followed by')

    class Meta:
        ordering = ['-created']

    # Short link must be validated for case-insensitive unique
    def clean(self):
        self.short_link = self.short_link.lower()
        if Event.objects.filter(short_link=self.short_link).exclude(id=self.id).count():
            raise ValidationError(u'%s is already used shortlink' % self.short_link)

    def get_future_dates(self):
        return self.event_dates.filter(
            start_date__gt=timezone.now()).order_by('start_date')

    def get_nearest_date(self, only_future=False):
        nearest_dates = self.event_dates.filter(end_date__gt=timezone.now()).order_by('start_date')
        if not nearest_dates.exists() and not only_future:
            nearest_dates = self.event_dates.order_by('-start_date')
        if nearest_dates.exists():
            return nearest_dates[0]
        return None

    def get_latest_date(self):
        return self.event_dates.all().first()

    def is_live_streaming(self, user=None):
        nowtime = timezone.now()
        if self.event_dates.filter(start_date__lt=nowtime, end_date__gt=nowtime).exists():
            return True
        return False

    def event_upload_images(self):
        return MultiuploaderImage.objects.filter(event_date__event_id=self.id)

    def thumb_url(self, size, size2):
        try:
            imgObject = get_thumbnail(self.main_image, str(size)+'x'+str(size2), crop='center', quality=99)
        except:
            return self.main_image.url
        urlImg = imgObject.url
        return urlImg

    @permalink
    def get_absolute_url(self):
        return 'view_event', None, {'slug': self.slug}


class EventImage(TimestampedModel):
    """
    Images For Events
    """
    latitude = models.FloatField(default=0.00, db_index=True)
    longitude = models.FloatField(default=0.00, db_index=True)
    image = ImageField(upload_to='event_images/')
    caption = models.CharField(max_length=100, blank=True)

    def __unicode__(self):
        return self.image.name

    @property
    def url(self):
        return self.image.url

    def thumb_url(self, size):
        return unicode(self.image.extra_thumbnails.get(size))
