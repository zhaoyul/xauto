# ---------------------------------------------------
# --- Django base core code (system)              ---
from django.core.urlresolvers import reverse
from django.db import models
from django.contrib.auth.models import User, _
from django.conf import settings
from django.db.models import Avg, Q
from django.contrib.gis.geos import point
from django.contrib.contenttypes.models import ContentType

# ---------------------------------
# -- Various Python libraries   ---
import datetime
from math import fabs
import string

# ---------------------------------------------------
# --- Django addon                                ---
#from livesettings.models import Setting
from livesettings import config_value
from sorl.thumbnail.fields import ImageField as ImageWithThumbnailsField
from sorl.thumbnail import get_thumbnail

from xauto_lib.models import TimestampedModel
from xauto_lib.orderable import OrderableModelMixin
from xauto_utils.video import VideoHelperFactory
from video.fields import YouTubeField
from xauto_lib.managers import manager_from
from xauto_lib.utils import convNumeric, CheckNumeric
from xauto_utils.calutil import convDatetimeToIsoDate
from xauto_utils.image_utils import *
from xauto_utils.logger import Reporter
from keywords.models import KeywordService

reporter = Reporter()

class Currency(models.Model):
    class Meta:
        verbose_name_plural = 'Currencies'
    country = models.CharField(max_length=64, unique=True)
    country_code = models.CharField(max_length=64, default='', blank=True, null=False, unique=False)
    currency = models.CharField(max_length=5)
    symbol = models.CharField(max_length=40, null=True)

    def get_currency(self):
        return self.symbol if self.symbol else ''
    currency_symbol = property(get_currency)

    def get_currency_name(self):
        return self.currency
    currency_name = property(get_currency_name)

    def get_symbol(self):
        return self.symbol if self.symbol else ''


    def __unicode__(self):
        return '%s: %s' % (self.country, self.currency)

# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# ---- E V E N T       D I S T A N C E      M A N A G E R                    ---
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------

class DistanceManager(models.Manager):
    """
    Search Events with a specific Distance and origin Geo Point
    Could provide following parameters
    user
    distance
    latitude
    longitude
    Distance unit(mode)
    Mysql Table (type)
    Order by
    """
    def within_radius(self, user=None, distance=9999, latitude=None, longitude=None, mode='mi', type='event', orderby=True):

        from member.models import UserProfile
        # ----------------------------------------------------
        # --- Currently we allow search on Event           ---
        # ----------------------------------------------------
        if type == 'event':
            object_list = Event.objects.all()    # --- Extract all available provider  ---

        selectedLatitude = 0.0
        selectedLongitude = 0.0
        selectedDistance = 0

        # ---------------------------------------
        # --- Database empty                  ---
        if not object_list:
            return object_list

        # -----------------------------------------------------------------------
        # --- Extract origin Point (Current Logged User, or provided Lat/long)---
        # -----------------------------------------------------------------------
        if not latitude or not longitude:
            # --------------------------------------------------------------
            # -- Not Geo Point  provided, try the Current User position ----
            try:
                if user:
                    profile = UserProfile.objects.get(user=user)
                    selectedLatitude = profile.latitude
                    selectedLongitude = profile.longitude
            except:
                return object_list
        else:
            # -----------------------------------------
            # --- Valid Point provided (Lat/Long) -----
            if CheckNumeric(latitude, wcheck='FLOAT') and CheckNumeric(longitude, wcheck='FLOAT'):
                selectedLatitude = convNumeric(latitude, wcheck='FLOAT')
                selectedLongitude = convNumeric(longitude, wcheck='FLOAT')
            else:
                return object_list

        # ----------------------------------------------------
        # --- Extract and Convert Distance to Km           ---
        # ----------------------------------------------------
        if distance:
            # -----------------------------------
            # -- No Distance Limit !!!        ---
            if distance == 'anywhere' or distance == 'all':
                distance = '9999'
            # ------------------------------------------------------------
            # -- Distance provided in miles format in Miles            ---
            if mode == 'mi':
                if distance.find('m') >=0:
                    distance= distance.replace('m', '')

        # ----------------------------------------
        # --- Check if Distance is Numeric     ---
        # --- In any case convert to Integer   ---
        if not CheckNumeric(distance):
            return object_list
        selectedDistance = convNumeric(distance, wcheck = 'INT')

        # ---------------------------------------------------------------------------------------
        # --- `Object_Distance` (50.459634, -3.526109, 50.459408, -3.524457)                  ---
        # ---  GeoDistDiff('km', 50.459634, -3.526109, 50.459408, -3.524457) as distance_km,  ---
        # ---  GeoDistDiff('mi', 50.459634, -3.526109, 50.459408, -3.524457) as distance_km,  ---
        # ---                                                                                 ---
        # ---   new formula. http://en.wikipedia.org/wiki/Geographical_distance               ---
        # ---   Ellipsoidal Earth projected to a plane                                        ---
        # ---   The FCC prescribes essentially the following formulae in 47 CFR 73.208        ---
        # ---   for distances not exceeding 475 km /295 miles:                                ---
        # ---------------------------------------------------------------------------------------

        if selectedDistance > 0 and fabs(selectedLatitude) > 0.0  and fabs(selectedLongitude) > 0.0:
            object_list = getDistance(mode, object_list, selectedLatitude, selectedLongitude, selectedDistance, orderby)
        else:
            if user:
                if not user.is_anonymous():
                    UserObject = UserProfile.objects.filter(user=user)
                    if UserObject:
                        userLatitude = UserObject[0].latitude
                        userLongitude = UserObject[0].longitude
                        userDistance = settings.RADIUS_NUMERIC
                        object_list = getDistance(mode, object_list, userLatitude, userLongitude, userDistance, orderby)

        return object_list

class DateDiffManager(models.Manager):
    def within_timediff(self, diff=24):
        event_list = Event.objects.all().filter(status='new')
        event_list = event_list.extra(select={'diff_time': """
            timediff(now(), published_at)
            """ })
        event_list = event_list.extra(where=["""
            timediff(now(), published_at) > %d
            """ % (diff)])
        event_list = event_list.extra(order_by=('title', ))
        return event_list


# -----------------------------------------------------------------------
# -----------------------------------------------------------------------
# ----            E V E N T                                           ---
# ----  EVENT DEFINITION / MANAGER / MODELS / QUERY SET               ---
# -----------------------------------------------------------------------
# -----------------------------------------------------------------------



class YoutubeVideoId(models.Model):
    video_id = models.CharField(max_length=255)
    event = models.ForeignKey('Event', related_name='youtube_videos')

    def __unicode__(self):
        return '%s' % self.video_id

class EventImage(models.Model):
    image = models.ImageField(upload_to=settings.EVENT_IMAGES_ROOT)
    event = models.ForeignKey('Event', related_name='images')
    latitude = models.FloatField(default=0.00, db_index=True)
    longitude = models.FloatField(default=0.00, db_index=True)

    def __unicode__(self):
        return '%s' % self.image.url

    def get_thumbnail_html(self, width, height=0):
        html = '<a class="image-picker" href="%s"><img width="%s" height="%s" src="%s"/></a>'
        return html % (self.image.url, width, height,  get_thumbnail_url(self.image.url, width))

    def get_thumbnail_dict(self):
        return dict(image_url=self.image.url,
                    thumbnail_url_130=get_thumbnail_url(self.image.url, 130),
                    thumbnail_url_310=get_thumbnail_url(self.image.url, 310),
                    thumbnail_url_48=get_thumbnail_url(self.image.url, 48),
                    id=self.id)

    get_thumbnail_html.short_description = _('thumbnail')
    get_thumbnail_html.allow_tags = True


class BaseEventQuerySet(models.query.QuerySet):

    def order_by_spec(self, *args, **kwargs):
        """
        Allow ordering to be set using presets in addition to the usual field
        specifications.
        """
        preset = kwargs.pop('preset', None)
        if SORT_PRESETS.has_key(preset):
            args += tuple(SORT_PRESETS[preset])
        else:
            preset = kwargs.pop('sort', None)
            if SORT_PRESETS.has_key(preset):
                args += tuple(SORT_PRESETS[preset])
        return super(BaseEventQuerySet, self).order_by(*args, **kwargs)

class EventQuerySet(BaseEventQuerySet):
    """
    Custom queryset class for event  manager.

    Hides draft, cancelled or otherwise invalid events.
    """
    def __init__(self, model=None, **kwargs):
        super(EventQuerySet, self).__init__(model=model, **kwargs)
        self.query.add_q(Q(status__in=(model.STATUS_NEW)))

class ActiveEventQuerySet(BaseEventQuerySet):
    """
    Custom queryset class for event  manager, selecting active events
    """
    def __init__(self, model=None, **kwargs):
        now = datetime.datetime.now()
        statusList = [Event.STATUS_NEW]
        super(ActiveEventQuerySet, self).__init__(model=model, **kwargs)
        self.query.add_q(Q(status__in=statusList))
        self.query.add_q(Q(expire_at__gt=now))

class EventManagerMixin(object):
    """
    Custom manager mixin for Event  model.
    """
    def active(self):
        """
        Return Public active Events.
        """
        statusList = [Event.STATUS_NEW]
        now = datetime.datetime.now()
        qs = self.filter(expire_at__gt=now, status__in=statusList)
        return qs

    def visible(self):
        """
        Return Events  that should be visible to site visitors, including active
        and ended Events .
        """
        statusList = [Event.STATUS_NEW]
        qs = self.filter(status__in=statusList)
        return qs



class EventDate(TimestampedModel):
    """
    Django models in relation with Event Models (Event Date)
    Start / End Date  - Price/Cost / featured
    """

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

    def __unicode__(self):
        return '(%s) - %s/%s' % (self.event.title.capitalize(), self.start_date, self.end_date)



class Organizer(TimestampedModel):
    """
    Django models in relation with Event Models (Event organizer)
    An Organizer could be Linked to a User (FK)
    Only one Event is linked to an Organizer
    Many Events could be linked to a single organizer (M2M)
    """

    organization_name = models.CharField(max_length=255, default='')
    organization_desc = models.TextField(null=True, blank=True, default='')
    events = models.ManyToManyField('Event', related_name='event_for_user', null=True, blank=True)
    venues = models.ManyToManyField('Venue', related_name='venue_for_user', null=True, blank=True)
    author = models.ForeignKey(User, related_name='organizer_event', verbose_name='User Who Organize the Event')
    event = models.ForeignKey('Event', null=True, blank=True, related_name='selected_organizer_event', verbose_name='Event related to this Event')
    remove_past_events = models.BooleanField(default=False)
    is_saved = models.BooleanField(default=False)
    include_social_link = models.BooleanField(default=False)
    shortname = models.CharField(max_length=250, default='')
    facebook_id = models.CharField(max_length=250, default='', null=True, blank=True)
    twitter_id = models.CharField(max_length=250, default='', null=True, blank=True)

    def __unicode__(self):
        return '%s - %s' % (self.organization_name, self.shortname)

class Venue(TimestampedModel):
    """
    Address for a given Organizer
    """

    organizer = models.ForeignKey(Organizer, related_name='organizer_venue', null=True, blank=True, verbose_name='Event Organizer')
    user = models.ForeignKey(User, related_name='user_venue', verbose_name='User who create the Venue')
    venue = models.CharField(max_length=50)
    address = models.CharField(max_length=100, default='', null=True, blank=True)
    address_2 = models.CharField(max_length=100, default='', null=True, blank=True)
    country = models.CharField(max_length=50,null=True, blank=True)
    country_short = models.CharField(max_length=50,null=True, blank=True)
    city = models.CharField(max_length=100,null=True, blank=True)
    state = models.CharField(max_length=50,null=True, blank=True)
    region = models.CharField(max_length=50,null=True, blank=True)
    zipcode = models.CharField(max_length=20, null=True, blank=True)
    latitude = models.FloatField(default=0.00)
    longitude = models.FloatField(default=0.00)
    longaddress = models.CharField(max_length=255)
    zoom = models.FloatField(default=0.00)
    is_saved = models.BooleanField(default=False)

    def __unicode__(self):
        return '%s-%s-%s' % (self.venue, self.city, self.country)

class Event(TimestampedModel):
    STATUS_NEW =  'new'
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
    description = models.TextField()
    keywords = models.ManyToManyField(KeywordService, related_name='user_keywords', null=True, blank=True)
    available_dates = models.ManyToManyField('EventDate', related_name='select_event_date', null=True, blank=True)

    author = models.ForeignKey(User, related_name='authored_event', null=True, blank=True)
    profile = models.ForeignKey('member.UserProfile', related_name='event_user_profile', null=True, blank=True)
    duration = models.PositiveIntegerField(default=0, verbose_name='Duration in Days')

    number = models.CharField(max_length=30, db_index=True, blank=True, null=True, verbose_name='Event Id')
    status = models.CharField(max_length=15, db_index=True, choices=STATUS_CHOICES, default=STATUS_NEW)
    eventSize = models.IntegerField(choices=EVENT_SIZE, default=10)  # How big is your event in Cars
    capacity = models.IntegerField(default=0)  # How big is your Capacity in people in people
    shortname = models.CharField(max_length=50, default='')
    venue = models.ForeignKey('Venue', on_delete=models.SET_NULL, blank=True, null=True, related_name='event_venue')
    organizer = models.ForeignKey('Organizer', on_delete=models.SET_NULL, blank=True, null=True, related_name='event_organizer')

    started_at = models.DateTimeField(null=True, blank=True , default=datetime.datetime.now())
    closed_at = models.DateTimeField(null=True, blank=True)
    archived_at = models.DateTimeField(null=True, blank=True)
    published_at = models.DateTimeField(auto_now_add=True)
    expire_at = models.DateTimeField(null=True)

    objects = DistanceManager()
    objtimes = DateDiffManager()
    main_image = models.ForeignKey('EventImageExtend', on_delete=models.SET_NULL, blank=True, null=True, related_name='main')
    video_cache = models.CharField(default='[]', max_length=255)
    youtube_url = YouTubeField(blank=True)
    video_url = models.URLField(null=True, blank=True)

    event_date = models.ManyToManyField(EventDate, related_name='available_date_for_your_event', null=True, blank=True, verbose_name='Available Event Date')
    followed = models.ManyToManyField('member.UserProfile', related_name='event_followed_user', null=True, blank=True, verbose_name='Event followed by')


    active = manager_from(EventManagerMixin, queryset_cls=ActiveEventQuerySet)   # -- pre-List Active Events ---
    valids = manager_from(EventManagerMixin, queryset_cls=EventQuerySet)

    google_analytics = models.CharField(default='', max_length=50)
    instructions = models.CharField(default='', max_length=250)


    @staticmethod
    def autocomplete_search_fields():
        return ("id__iexact", "title__icontains",)

    def __unicode__(self):
        if self.venue:
            if self.venue.region:
                return '%s, %s, %s' % (self.title, self.venue.city, self.venue.region)
            else:
                return '%s, %s, %s' % (self.title, self.venue.city, self.venue.country)
        else:
            return '%s' % (self.title)

    def get_video_thumbnail(self):
        return VideoHelperFactory.get_helper(self.video_url).get_thumbnail_link()

    def get_video_embed_url(self):
        return VideoHelperFactory.get_helper(self.video_url).get_embed_url()

    def raw_remaining_time(self):
        rem = self.expire_at - datetime.today()
        return rem.seconds

    def remaining_time(self):
        rem = self.expire_at - datetime.today()
        hours, remainder = divmod(rem.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        if rem.days == 0:
            return '%dh %dmin' % (hours, minutes)
        else:
            if rem.days == 1:
                return '1 Day %dh %dmin' % (hours, minutes)
            else:
                return '%s days' % (rem.days)

    def getShortLocation(self, sep=',', mode='array'):

        sep = ''
        if mode == 'array':
            retAddress= []
        else:
            retAddress = ''

        if self.venue:
            venueObj = self.venue

            if venueObj.address:
                if mode == 'array':
                    retAddress.append(venueObj.address)
                else:
                    retAddress += venueObj.address

            if venueObj.city:
                if mode == 'array':
                    retAddress.append(venueObj.city)
                else:
                    sep = ''
                    if retAddress != '':
                        sep = '<br/>'
                    retAddress += sep + venueObj.city

            if venueObj.state:
                if mode == 'array':
                    retAddress.append(venueObj.state)
                else:
                    if venueObj.city:
                        sep = ' '
                    retAddress += sep + venueObj.state

            if venueObj.zipcode:
                if mode == 'array':
                    retAddress.append(venueObj.zipcode)
                else:
                    sep = ''
                    if venueObj.city or venueObj.state:
                        sep = ' '
                    retAddress += sep + venueObj.zipcode

            if venueObj.country:
                if mode == 'array':
                    retAddress.append(venueObj.country)
                else:
                    sep = ''
                    if retAddress != '':
                        sep = '<br/>'
                    retAddress += sep + venueObj.country

        if mode == 'array':
            return string.join(retAddress, sep)
        else:
            return retAddress

    @property
    def getRemainingTime(self):
        """
        convDatetimeToIsoDate
        dayDifference

        """

        date_format = '%Y-%m-%d %H:%M'
        currentDate = convDatetimeToIsoDate(datetime.datetime.now())
        expireDate = convDatetimeToIsoDate(self.expire_at)

        fromDate = datetime.strptime(currentDate, date_format)
        toDate = datetime.strptime(expireDate, date_format)

        # -----------------------------------------------------------
        # -- compute ramining duration in days, Hours and minutes ---
        rem = toDate - fromDate
        days = rem.days
        hours, remainder = divmod(rem.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        labelDay = 'days'
        labelHour = 'h'

        # -------------------------------------------
        # --- compute Round for days above 3 days ---
        if days >= 3:
            if hours >= 12:
                days  += 1
                hours = ''

        # --------------------------
        # -- less than 1 days     --
        if days == 0:
            return '%dh %dmin' % (hours, minutes)

        # --------------------------------------
        # --- negative value, expired event !! ---
        elif days < 0:
            return '0 days'

        # --------------------------------------------------
        # -- more than 1 Days, display  nn days, Nn Hours --
        else:
            if days == 1:
                labelDay = 'day'
            if hours != '' and hours != '0':
                return '%s %s, %s%s'  % (days, labelDay, hours, labelHour)
            else:
                return '%s %s'  % (days, labelDay)

    @property
    def getEventImage(self):
        from multiuploader.models import MultiuploaderImage
        items = None
        try:
            eventObj = self
            items = MultiuploaderImage.objects.filter(event=eventObj)
            if items:
                return items[0]
        except:
            pass
        return items


    def EVENT_IMAGE(self):
        from multiuploader.models import MultiuploaderImage
        items = None
        try:
            eventObj = self
            items = MultiuploaderImage.objects.filter(event=eventObj)
            if items:
                imageRecord = items[0]
                imgObject = get_thumbnail(imageRecord, '50x50', crop='center', quality=99)
                urlImg = imgObject.url
                htmlDiv = '<img src="%s"/>' % urlImg
                return htmlDiv
        except:
            pass
        return  '<img src="%s"/ width="50"  height="50">' % ('/static/images/default_pic.jpg')

    EVENT_IMAGE.allow_tags = True


    def coloredEventStatus(self):

        colorCode = 'blue'
        if self.status == 'closed':
            colorCode = 'red'
        return '<span style="color: %s;">%s</span>' % (colorCode, self.status)
    coloredEventStatus.allow_tags = True

    @property
    def getFeedbacksFromOrganizer(self):
        """
        Get feedbacks from customer for all Events of this Event
        """
        feedbackList = Feedback.objects.filter(event=self, feedback_mode='organizer')
        if feedbackList:
            return feedbackList
        return None

    def ratings_for_this_event(self):
        try:
            f_ratings = FeedbackRating.active.all().filter(Q(event=self) & Q(author=self.author))
            avgRatingEvent = [{'name': rating_val.rate_type.name, 'value': rating_val.rating } for rating_val in f_ratings]
            return avgRatingEvent
        except Exception:
            return None

    @property
    def getEventStatus(self):
        #STATUS_CHOICES
        dicStatusLabel = Event.LABEL_STATUS_CHOICES
        if self.status in dicStatusLabel:
            eventStatus = dicStatusLabel[self.status]
            if eventStatus == 'Awarded':
                eventStatus = '%s' % (eventStatus)
        else:
            eventStatus = '*N/A*'
        return eventStatus

    def get_total_rating(self):
        import decimal
        D=decimal.Decimal
        rating = FeedbackRating.active.filter(event=self).aggregate(average_rating=Avg('rating'))
        if rating['average_rating']:
            ratingValue = rating['average_rating']
        else:
            ratingValue = 0
        RatingValue = round(ratingValue,0)
        if ratingValue <= 0.5 and ratingValue > 0.1:
            ratingValue = 1
        return ratingValue

    def get_currency_symbol(self):
        if not hasattr(self, '_currency_symbol'):
            self._currency_symbol = self.currency.currency_symbol
        return self._currency_symbol

    def get_currency_name(self):
        if not hasattr(self, '_currency_name'):
            self._currency_name = self.currency.currency_name
        return self._currency_name

    def detailed_view_link(self):
        return settings.NOMINAL_URL + reverse('view_event') + str(self.id)

    def get_location(self):
            # Remember, longitude FIRST!
            return point.Point(self.longitude, self.latitude)


    def save(self,  *args, **kwargs):

        if not self.number or  self.number == '00000':
            # -------------------------------------
            # ----- Computer Job Public Number ----
            # --- Author Id + Job Id + Seq Id ---
            last_number = config_value('EVENT','NUMBER')
            if not last_number:
                last_number = 1
            last_number += 1
            #objSettings = Setting.objects.filter(group='EVENT', key='NUMBER').update(value=last_number)

            # -------------------------------------
            # -- format and save the Bid Number ---
            self.number = '%s-%04d' % (self.shortname, last_number)
        super(Event, self).save(**kwargs)



# ----------------------------------------------------------------------------
# ----------------------------------------------------------------------------
# ----  R A T I N G     A N D   F E E D B A C K      F O R     E V E N T   ---
# ----  FEEDBACK DEFINITION / MANAGER / MODELS / QUERY SET                 ---
# ----------------------------------------------------------------------------
# ----------------------------------------------------------------------------


class ActiveFeebackQuerySet(BaseEventQuerySet):
    """
    Custom queryset class for event  manager, selecting active events
    """
    def __init__(self, model=None, **kwargs):
        super(ActiveFeebackQuerySet, self).__init__(model=model, **kwargs)
        #self.query.add_q(Q(xxxxx=True))

class ActiveFeebackQuerySetRoot(BaseEventQuerySet):
    """
    Custom queryset class for Event   manager, selecting active events
    """
    def __init__(self, model=None, **kwargs):
        super(ActiveFeebackQuerySetRoot, self).__init__(model=model, **kwargs)
        self.query.add_q(Q(event__feedback_customer_left=True))
        self.query.add_q(Q(event__feedback_provider_left=True))

class FeedbackManagerMixin(object):
    """
    Custom manager mixin for Feedback and FeedbackRating  model.
    """
    def active(self):
        """
        Return Public Feedback left (customer or provider).
        """
        qs = self.filter(event__feedback_customer_left=True, event__feedback_provider_left=True)
        return qs

class Feedbackextended(models.Manager):
    def get_queryset(self):
        return super(Feedbackextended, self).get_queryset().filter(event__feedback_customer_left=True, event__feedback_provider_left=True)

class FeedbackextendedB(models.Manager):
    def get_queryset(self):
        return super(FeedbackextendedB, self).get_queryset().filter(event__feedback_customer_left=True, event__feedback_provider_left=True)


class FeedbackManagerMixinRoot(object):
    """
    Custom manager mixin for Feedback and FeedbackRating  model.
    """
    def active(self):
        """
        Return Public Feedback left (customer or provider).
        """
        qs = self.filter(event__feedback_customer_left=True, event__feedback_provider_left=True)
        return qs

class Feedback(TimestampedModel):
    """
    Django models in relation with Event Models (add updates on model)
    """

    RATING_STATUS_CHOICES = (
        ('complete', 'Complete'),
        ('progress', 'In progress'),
    )

    RATING_MODE = (
        ('customer', 'Customer'),
        ('provider', 'Provider'),
    )


    comment = models.TextField(null=True, blank=True, default='')
    event = models.ForeignKey('Event', related_name='event_feedback')
    author = models.ForeignKey(User, related_name='feedback_author', verbose_name='User Who receives the ratings')  # user who received the ratings
    given_author = models.ForeignKey(User, null=True, blank=True, related_name='given_feedback_author', verbose_name='User Who gives the ratings')
    send_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    rating = models.ManyToManyField('FeedbackRating', null=True, blank=True, related_name='feedback_list_rating')
    feedback_status = models.CharField(max_length=50,choices=RATING_STATUS_CHOICES, default='')
    feedback_mode = models.CharField(max_length=50,choices=RATING_MODE, default='customer')
    recommend = models.BooleanField(default=True)
    active = manager_from(FeedbackManagerMixinRoot, queryset_cls=ActiveFeebackQuerySetRoot)   # -- pre-List Active Events ---
    objects = models.Manager()

    def __unicode__(self):
        return '%s - %s' % (self.author.username, self.comment[:50] + ('...' if len(self.comment) > 50 else ''))

    @property
    def getAvgFeedback(self):
        """
        get average feedback (all retaing type)
        """
        avgRatings = self.rating.all().aggregate(average_rating=Avg('rating'))
        if avgRatings:
            avg_rating_value= avgRatings['average_rating']
            return avg_rating_value
        else:
            return 0


class RatingValue(TimestampedModel):
    """
    add fix for new xauto ratings system
    """
    name = models.CharField(max_length=32)
    index = models.IntegerField(default=1)
    keyword = models.CharField(max_length=32, default='')
    order = models.IntegerField(default=1)

    def __unicode__(self):
        return '%s' % self.name

class FeedbackRating(TimestampedModel):
    RATING_CHOICES = (
        (0.0, 0),
        (1.0,1),
        (1.5,1.5),
        (2.0,2),
        (2.5,2.5),
        (3.0,3),
        (3.5,3.5),
        (4.0,4),
        (4.5,4.5),
        (5,5))

    rate_type = models.ForeignKey(RatingValue)
    rating = models.FloatField(choices=RATING_CHOICES, default=0)
    author = models.ForeignKey(User, related_name='rating_author', blank=True, null=True)
    event = models.ForeignKey('Event', related_name='feedbackrating_event' ,blank=True, null=True)
    active = manager_from(FeedbackManagerMixin, queryset_cls=ActiveFeebackQuerySet)   # -- pre-List Active Events ---
    objects = models.Manager()

    def __unicode__(self):
        return '%s-%s-%s' % (round(self.rating, 1),  self.rate_type, self.event)

    def save(self, **kwargs):
        """
        """

        from member.models import UserProfile
        super(FeedbackRating, self).save(**kwargs)

        # -----------------------------------------------------
        # -- global update of all user's feedback           ---
        countReview = Feedback.objects.filter(Q(author=self.author) & Q(event__status=Event.STATUS_COMPLETE)).count()

        # -------------------------------------------------------------------------------
        # ------------ Update average Global ratings for the current User ---------------
        avgRatings = FeedbackRating.active.filter(author=self.author).aggregate(average_rating=Avg('rating'))
        if avgRatings:
            avg_rating_value= avgRatings['average_rating']

        # -------------------------------------------------------
        # ------ detail average ratings by each rating type -----
        dicRate = {}
        arrayRateType = RatingValue.objects.all()
        for eachtypeRate in arrayRateType:
            avgRatings = FeedbackRating.active.filter(author=self.author, rate_type=eachtypeRate).aggregate(average_rating=Avg('rating'))
            if avgRatings:
                if avgRatings['average_rating']:
                    dicRate[eachtypeRate.keyword] = avgRatings['average_rating']
                else:
                    dicRate[eachtypeRate.keyword] = 0.0

        # --------------------------------------------
        # ---- final save on userProfile database ----
        userObject = UserProfile.objects.get(user=self.author)
        if userObject:
            userObject.reviews = countReview
            userObject.avg_ratings = round(avg_rating_value,0)
            userObject.avg_ratings_professionalism = dicRate.get('professionalism')
            userObject.avg_ratings_knowledge  = dicRate.get('knowledge')
            userObject.avg_ratings_efficiency = dicRate.get('efficiency')
            userObject.avg_ratings_expense = dicRate.get('expense')
            userObject.avg_ratings_quality = dicRate.get('quality')
            userObject.save()



class EventImageManager(models.Manager):
    """
    Custom manager for Event images
    """
    def main_for_events(self, event_ids):
        """
        Select main image for each event in given list
        """
        return self.filter(event__id__in=event_ids)


class EventImageExtend(TimestampedModel, OrderableModelMixin):
    """
    Images For Events
    """
    event = models.ForeignKey('Event', related_name='event_images')
    latitude = models.FloatField(default=0.00, db_index=True)
    longitude = models.FloatField(default=0.00, db_index=True)
    image = ImageWithThumbnailsField(upload_to='event_images/')
    caption = models.CharField(max_length=100, blank=True)
    objects = EventImageManager()


    def __unicode__(self):
        return self.image.name

    @property
    def url(self):
        return self.image.url

    def thumb_url(self, size):
        return unicode(self.image.extra_thumbnails.get(size))

    def copy_into(self, new_event):
        from django.core.files.images import ImageFile

        new_obj = self._default_manager.create(
            event=new_event,
            caption=self.caption,
            image=ImageFile(self.image))
        return new_obj


class flagEvent(TimestampedModel):
    """
    Flag an Event
    """

    event = models.ForeignKey('Event', related_name='flag_an_event')
    author = models.ForeignKey(User, related_name='flag_ad_author')
    reason = models.CharField(max_length=100, blank=False, null=False, default='')
    description = models.CharField(max_length=1024, blank=True, null=True, default='')
    active = models.BooleanField(default=True)
    email_sent = models.BooleanField(default=False)
    message_sent = models.BooleanField(default=False)
    review = models.BooleanField(default=False)
    remove_event = models.BooleanField(default=False)
    date_email = models.DateTimeField(null=True, blank=True)
    date_review = models.DateTimeField(null=True, blank=True)
    answers = models.ManyToManyField('member.Message', related_name='flag_ad_messages', null=True, blank=True)
    response = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return '%s-%s' % (self.event.title, self.reason)

# ------------------------------------------------------------------------
# ------------------------------------------------------------------------
# --- Event various sub-routines                                      ----
# ------------------------------------------------------------------------
# ------------------------------------------------------------------------

def logStat(currentObjRecord, event, type, target, country='US'):
    """
    API method for logging statistics.
    """

    """
    event_stat  = models.CharField(choices=STATISTIC_CHOICES, max_length=55, null=True, blank=True, default='search')
    type_stat  = models.CharField(choices=STATISTIC_OBJECT, max_length=55, null=True, blank=True, default='keyword')
    target_stat  = models.CharField(choices=TARGET_OBJECT, max_length=55, null=True, blank=True, default='keyword')
    count_stat = models.IntegerField(default=0) # count access on this Object/event
    content_type = models.ForeignKey(ContentType, blank=True, null=True)
    object_id = models.PositiveIntegerField(blank=True, null=True)
    """
    try:
        objRecord = currentObjRecord[0]
    except:
        objRecord = currentObjRecord

    if objRecord:
        objStat = Statistics.objects.filter(country=country, event_stat=event, type_stat= type, target_stat= target, object_id=objRecord.id)
        if not objStat:
            objStat = Statistics.objects.create (
                event_stat=event,
                type_stat= type,
                target_stat = target,
                count_stat = 1,
                content_type =  ContentType.objects.get_for_model(objRecord),
                content_object = objRecord,
                country = country,
                object_id = objRecord.id
            )
            return objStat
        else:
            statRecord = objStat[0]
            currentCount = statRecord.count_stat
            currentCount += 1
            statRecord.count_stat = currentCount
            statRecord.save()
            return statRecord
    return None


def storeKeywordStat(request, mainList,  keywordsList, typeStat, userprofile, selectedKeyword=''):
    """
    Store Most Popular Used keywords
    """

    from context_processors import request_data

    if mainList:

        try:
            countryCode = userprofile.country
        except:
            userdata = request_data(request)
            countryCode = userdata['country_short']

        # ---- extract all keywords attached to the Object  List ---
        arrayExtractkeywords = []
        dicKeywords = {}
        for eachUser in mainList:
            for eachKeywords in eachUser.keywords.all():
                if eachKeywords not in dicKeywords:
                    dicKeywords[eachKeywords] = 1

        # --- finds keyword really used for this search ---
        for keywordObj in keywordsList:
            if keywordObj in dicKeywords:
                objStat = logStat(keywordObj, 'search', 'keyword', typeStat, country=countryCode)
                selectedKeyword += keywordObj.keyword

    return selectedKeyword

def getDistance(mode, object_list, selectedLatitude, selectedLongitude, selectedDistance, orderby):
    """
    Get distance object for a given Ip location
    """
    # ---- prepare  select  distance statement  ---
    object_list = object_list.extra(select={'distance': """
        GeoDistDiff('%s', %f, %f, latitude, longitude)
        """ % (mode, selectedLatitude, selectedLongitude)})
    # --- prepare Where distance statement     ---
    if selectedDistance:    #and distance != 200
        object_list = object_list.extra(where=["""
        GeoDistDiff('%s', %f, %f, latitude, longitude) <= %d+0.003
        """ % (mode, selectedLatitude, selectedLongitude, selectedDistance)])
    # --- prepare Distance Sort By if required ---
    if orderby:
        object_list = object_list.extra(order_by=('distance', ))

    return object_list
