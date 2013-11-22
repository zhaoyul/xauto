# ---------------------------------------------------
# --- Django base core code (system)              ---
# ---------------------------------------------------
from django.core.urlresolvers import reverse
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg, Count, Q, Max
from geoip2.models import Country
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType

# ---------------------------------
# -- Various Python libraries   ---
# ---------------------------------
import socket
import struct
import string

# ---------------------------------------------------
# --- Django addon                                ---
# ---------------------------------------------------
from sorl.thumbnail.fields import ImageField as ImageWithThumbnailsField

# ---------------------------------------------------
# --- Xauto Data models                           ---
# ---------------------------------------------------
from event.models import Event
from xauto_lib.models import TimestampedModel
from xauto_lib.orderable import OrderableModelMixin
from xauto_utils.video import VideoHelperFactory
from video.fields import YouTubeField
from xauto_utils.image_utils import *
from xauto_utils.logger import Reporter
from keywords.models import KeywordService

reporter = Reporter()

class memberStat(models.Model):

    type_stat = models.CharField(max_length=255)             # Event, keywords, ...
    member_view_count = models.IntegerField(default=0)       # cache
    member_contact_count = models.IntegerField(default=0)    # cache
    from_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)


class Statistics(TimestampedModel):
    """
    Django models to store various statistics (User, search, Event, ...)
    """
    STATISTIC_CHOICES = (
        ('search', 'Search'),
    )
    STATISTIC_OBJECT = (
        ('keyword', 'Keyword'),
    )
    TARGET_OBJECT = (
        ('provider', 'Providers'),
        ('work', 'Works'),
    )

    event_stat  = models.CharField(choices=STATISTIC_CHOICES, max_length=55, null=True, blank=True, default='search')
    type_stat  = models.CharField(choices=STATISTIC_OBJECT, max_length=55, null=True, blank=True, default='keyword')
    target_stat  = models.CharField(choices=TARGET_OBJECT, max_length=55, null=True, blank=True, default='work')
    count_stat = models.IntegerField(default=0)                             # count access on this Object/event
    content_type = models.ForeignKey(ContentType, blank=True, null=True)
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    country = models.CharField(max_length=255, null=True, blank=True, default='US')

    object_id = models.PositiveIntegerField(blank=True, null=True)

    def __unicode__(self):
        return '%s - %s - %s' % (self.type_stat, self.target_stat, self.object_id)



class MessageThread(TimestampedModel):
    """
    All related message Messages to a root messages
    """

    STATUS_THREAD_CHOICES = (
        ('root', 'root'),
        ('child', 'child')
    )

    sender = models.ForeignKey(User, related_name='member_sent_messages_thread', null=True, blank=True)
    recipient = models.ForeignKey(User, related_name='member_received_messages_thread', null=True, blank=True)
    sent_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True)
    respond_at = models.DateTimeField(null=True, blank=True)
    sequence = models.IntegerField(default=1)
    status_thread = models.CharField(choices=STATUS_THREAD_CHOICES, max_length=30, default='root', db_index=True)
    root_message = models.ForeignKey('Message', related_name='root_message_key', null=True, blank=True)
    message = models.TextField()

    def __unicode__(self):
        return '(%s) %s -> %s (%s)' % (self.id, self.status_thread, self.sent_at, self.sequence)

    @property
    def getsendername(self):
        senderName = '%s %s' % (self.sender.first_name.capitalize(), self.sender.last_name.capitalize())
        return senderName


class Message(TimestampedModel):
    """
    Messages processing between Users, Event organizers
    """
    EVENT_CREATED = 'event_created'
    FLAGEVENT = 'event_flagged'
    XAUTO_NEWS = 'snews'

    MESSAGE_SUBJECT = {
        EVENT_CREATED :  'Congrats you have successfully created and posted a New event.',
        }

    MESSAGE_TYPE = (
        (EVENT_CREATED, 'Event Created'),
    )

    STATUS_NEW = 'new'
    STATUS_DRAFT = 'draft'
    STATUS_REMOVE = 'remove'
    STATUS_CHOICES = (
        ('new', 'New'),
        ('draft', 'Draft'),
        ('remove', 'Removed')
    )

    ORIGIN_MESSAGE = (
        ('organizer', 'Organizer'),
        ('attendee', 'Attendee'),
        ('alert', 'Alert'),
        ('system', 'system')
    )

    # --- Categories of Messages ------
    MESSAGE_ALERT = ['alert', 'system', ]
    MESSAGE_SYSTEM = [XAUTO_NEWS, ]

    event = models.ForeignKey(Event, related_name="member_event_messages", null=True, blank=True)
    sender = models.ForeignKey(User, related_name='member_sent_messages', null=True, blank=True)
    recipient = models.ForeignKey(User, related_name='member_received_messages', null=True, blank=True)
    type = models.CharField(choices=MESSAGE_TYPE, max_length=30, default=EVENT_CREATED)
    chain_start = models.ForeignKey('self', null=True, blank=True, related_name='chain')
    read = models.BooleanField(default=False)
    subject = models.CharField(max_length=255)
    origin = models.CharField(choices=ORIGIN_MESSAGE, max_length=40, default='')     # --- Message origin Customer, Provider , xauto ---
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(choices=STATUS_CHOICES, max_length=30, default='new', db_index=True)
    removed_by = models.IntegerField(default=0)
    email = models.BooleanField(default=True)            # --- send message by email (+) ---
    attached = models.BooleanField(default=False)        # -- File attached to this message ---
    threads = models.ManyToManyField(MessageThread, related_name='message_chained_threads')
    joined_files = models.ManyToManyField('multiuploader.MultiuploaderFiles', related_name='message_joinded_files')
    content_objtect = generic.GenericForeignKey('content_type', 'object_id')
    content_type = models.ForeignKey(ContentType, blank=True, null=True)
    object_id = models.PositiveIntegerField(blank=True, null=True)
    deleted = models.CharField(max_length=2, default='')
    archived = models.CharField(max_length=2, default='')

    def __unicode__(self):
        if self.recipient:
            return '[%s] %s -> %s (%s) (%s) (%s)' % (self.sent_at, self.sender,  self.recipient, self.subject, self.type, self.status)
        else:
            if self.subject:
                return '[%s] %s (%s) (%s) (%s)' % (self.sent_at, self.sender, self.subject, self.type, self.status)
            else:
                return '[%s] %s (%s) (%s)' % (self.sent_at, self.sender, self.type, self.status)

    def sent_direction(self):
        return '%s -> %s' % (self.sender, self.recipient)
    sent_direction.short_description = 'Sent'

    @property
    def getArchived(self):
        if self.archived:
            return 'y'
        return ''


    def short_message(self):
        return self.message[:20] + ('...' if len(self.message) > 20 else '')
    short_message.short_description = 'Message'

    @property
    def getsendername(self):
        senderName = '%s %s' % (self.sender.first_name.capitalize(), self.sender.last_name.capitalize())
        return senderName

    @property
    def getLastMessage(self):
        """
        get last available message
        """
        if self.threads.all():
            lastSequence = self.threads.all().aggregate(maxseq=Max('sequence'))
            maxSeq = lastSequence['maxseq']
            lastMsg = self.threads.filter(sequence=maxSeq)
            return lastMsg[0]
        else:
            return self

    @property
    def getAttachedFile(self):
        """
        Return first attached File
        """

        from multiuploader.models import MultiuploaderFiles
        fileName =''
        if self.attached:
            attachObject = MultiuploaderFiles.objects.filter(message=self)
            if attachObject:
                fileName = attachObject[0].filename
                return fileName
        return fileName


    def type_str(self):
        return self.get_type_display()


class MessageView(models.Model):
    message = models.ForeignKey(Message, related_name='views')
    user = models.ForeignKey(User, related_name='viewed_messages')
    view_at = models.DateTimeField(auto_now_add=True)

class RecoveryQuestion(models.Model):
    question = models.CharField(max_length=255)

    def __unicode__(self):
        return self.question


class UserProfileManager(object):
    """
    Custom manager mixin for User Profile.
    """

    def getProviderRating(self):
        user_id = self.user
        rating = FeedbackRating.active.all().filter(Q(feedback__event__author=user_id) & Q(feedback__event__status=Event.STATUS_COMPLETE )).aggregate(average_rating=Avg('rating'))
        return rating['average_rating'] if rating['average_rating'] else 0

class UserProfileManager2(models.Manager):
    """
    Custom manager for Userprofile only active members.
    """
    def get_query_set(self):
        return super(UserProfileManager, self).get_query_set().filter(user__is_active=True)

    def top_sellers(self):
        """
        Return members queryset sorted by number of completed sales.
        """
        return self.annotate(num_sales=Count('sales')).order_by('-num_sales')

    def getProviderRating(self):
        user_id = self.user
        rating = self.filter(Q(feedback__event__author=user_id) & Q(feedback__event__status=Event.STATUS_COMPLETE)).annotate(average_rating=Avg('rating_author__rating'))

        return rating['average_rating'] if rating['average_rating'] else 0


class GeoLiteCityLocation(TimestampedModel):
    """
    City maxmind Database
    """

    loc_id = models.BigIntegerField(default=0, db_index=True, primary_key=True)
    country = models.CharField(max_length=2, null=True, blank=True, db_index=True)  # country code
    region = models.CharField(max_length=2, null=True, blank=True)  # choices=MESSAGE_TYPE
    city = models.CharField(max_length=255, null=True, blank=True, db_index=True)  # choices=MESSAGE_TYPE
    postal_code = models.CharField(max_length=6, null=True, blank=True, db_index=True)  # choices=MESSAGE_TYPE
    latitude = models.FloatField(default=0.00, db_index=True)
    longitude = models.FloatField(default=0.00, db_index=True)
    metro_code = models.IntegerField(default=0)
    area_code = models.CharField(max_length=3, null=True, blank=True)  # choices=MESSAGE_TYPE


    def __unicode__(self):
        return '%s-%s-%s' % (self.localId, self.country, self.city)



class userLanguage(TimestampedModel):
    """
    language available
    """

    code = models.CharField(max_length=50, null=True, blank=True, db_index=True)
    language = models.CharField(max_length=50, null=True, blank=True, db_index=True)
    description = models.CharField(max_length=255, null=True, blank=True)

    def __unicode__(self):
        return '%s-%s' % (self.code, self.language)


class duplicateEmails(TimestampedModel):
    """
    check duplicated emails
    """

    subject = models.CharField(max_length=255, null=True, blank=True, db_index=True)
    recipient = models.CharField(max_length=100, null=True, blank=True, db_index=True)
    from_email = models.CharField(max_length=100, null=True, blank=True, db_index=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    sending_day = models.CharField(max_length=5, default='')
    event = models.ForeignKey(Event, related_name='duplicated_event_email', null=True, blank=True)

    def __unicode__(self):
        return '%s-%s' % (self.subject, self.sent_at)


class GeoLiteCountryBlock(TimestampedModel):
    """
    Country whois by Ip address
    """

    start_ip = models.CharField(max_length=20, null=True, blank=True, db_index=True)  # start ip
    end_ip = models.CharField(max_length=20, null=True, blank=True)  # end IP
    begin_ip_num  = models.BigIntegerField(default=0, db_index=True)
    end_ip_num  = models.BigIntegerField(default=0, db_index=True)
    country_code = models.CharField(max_length=4, null=True, blank=True, db_index=True)  # country code
    country = models.CharField(max_length=50, null=True, blank=True, db_index=True)  # country label
    currency  = models.ForeignKey('event.Currency', null=True, blank=True, db_index=True)  # country currency default

    def __unicode__(self):
        return '%s-%s' % (self.country_code, self.country)


def inet_aton(ip):
    """ Convert string IP representation to integer
    """
    return struct.unpack('!L', socket.inet_aton(ip))[0]



class GeoLiteCityBlockManager(models.Manager):

    def by_ip(self, ip):
        """ Find the smallest range containing the given IP.
        """
        try:
            number = inet_aton(ip)
        except Exception:
            raise GeoLiteCityBlock.DoesNotExist

        try:
            return super(GeoLiteCityBlockManager, self).get_query_set()\
                                              .filter(begin_ip_num__lte=number, end_ip_num__gte=number)[0]

        except IndexError:
            raise GeoLiteCityBlock.DoesNotExist


class GeoLiteCityBlock(models.Model):
    """
    City Block  / Ip range
    """

    begin_ip_num  = models.BigIntegerField(default=0, db_index=True)
    end_ip_num  = models.BigIntegerField(default=0, db_index=True)
    local = models.ForeignKey(GeoLiteCityLocation, related_name="city_location", null=True, blank=True)
    objects = GeoLiteCityBlockManager()

    def __unicode__(self):
        return '%s' % (self.local_id)


    @property
    def getCity(self):
        """
        Get City Information
        """
        if self.local:
            currentCity =  self.local.city
            return currentCity
        return ''

    @property
    def getRegion(self):
        """
        Get region  Information
        """
        if self.local:
            currentRegion =  self.local.region
            return currentRegion
        return ''

    @property
    def getCountry(self):
        """
        Get Country Information
        """
        if self.local:
            country  =  self.local.country
            if country:
                objCountry = Country.objects.get(code=country)
                return objCountry.name
        return ''

    @property
    def getCountryShort(self):
        """
        Get Country Information by code
        """
        if self.local:
            currentCountry =  self.local.country
            return currentCountry
        return ''


class Comments(models.Model):
    comment = models.TextField()
    author = models.ForeignKey('UserProfile', related_name='userprofile_comments')
    send_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    score = models.IntegerField(null=True, blank=True, default=0)
    event = models.ForeignKey('event.Event', related_name='event_comments')

    def __unicode__(self):
        return '%s - %s' % (self.author.name, self.comment[:50] + ('...' if len(self.comment) > 50 else ''))


class UserProfile(TimestampedModel):

    PROFILE_TYPE = (
        ('video', 'Link Viedo'),
        ('image', 'Link Picture') )


    user = models.OneToOneField(User, related_name='profile')
    name = models.CharField(max_length=255, null=True, blank=True)  # choices=MESSAGE_TYPE
    media_mode = models.CharField(choices=PROFILE_TYPE, max_length=30, null=True, blank=True, default='image')
    location_address = models.CharField(max_length=255, null=True, blank=True)
    ip_location = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=30, null=True, blank=True)
    zipcode = models.CharField(max_length=10, null=True, blank=True)
    region = models.CharField(max_length=50, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    reviews = models.IntegerField(default=0, null=True, blank=True)
    avg_ratings = models.FloatField(default=0.0, null=True, blank=True, verbose_name='Average Rating')
    avg_ratings_professionalism = models.FloatField(default=0.0, null=True, blank=True, verbose_name='Average Professionalism Rating')
    avg_ratings_knowledge  = models.FloatField(default=0.0, null=True, blank=True, verbose_name='Average Knowledge  Rating')
    avg_ratings_efficiency = models.FloatField(default=0.0, null=True, blank=True, verbose_name='Average Efficiency Rating')
    avg_ratings_expense = models.FloatField(default=0.0, null=True, blank=True, verbose_name='Average Expense Rating')
    avg_ratings_quality = models.FloatField(default=0.0, null=True, blank=True, verbose_name='Average Quality Rating')
    event_count = models.IntegerField(default=0)
    events = models.ManyToManyField('event.Event', related_name='event_for_member', null=True, blank=True, verbose_name='Followed events')

    currency = models.ForeignKey('event.Currency', null=True, blank=True)
    language = models.ForeignKey(userLanguage, null=True, blank=True)
    last_notification_sent_at = models.DateTimeField(null=True, blank=True)
    question = models.ForeignKey(RecoveryQuestion, null=True, blank=True)
    answer = models.CharField(max_length=255, null=True, blank=True)
    about = models.TextField(null=True, blank=True, verbose_name='Service About')
    about_customer = models.TextField(null=True, blank=True, verbose_name='Customer About')
    keywords = models.ManyToManyField(KeywordService, related_name='profile_keywords')

    comments = models.ManyToManyField('Comments', null=True, blank=True, related_name='profile_user_comments')
    main_image = models.CharField(max_length=255, null=True, blank=True)
    images = models.ManyToManyField('multiuploader.MultiuploaderImage', null=True, blank=True, related_name='profile_images')
    youtube_url = YouTubeField(blank=True)
    video_url = models.URLField(null=True, blank=True)
    is_organizer = models.BooleanField(default=False)
    is_attendee = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    is_suspended = models.BooleanField(default=False)
    is_closed = models.BooleanField(default=False)
    reason_suspended = models.CharField(max_length=255, null=True, blank=True)
    reason_closed = models.CharField(max_length=255, null=True, blank=True)
    date_closed = models.DateTimeField(null=True, blank=True)

    ratings = UserProfileManager()

    def __unicode__(self):
        if self.region:
            return '%s, %s, %s' % (self.name, self.city, self.region)
        else:
            return '%s, %s, %s' % (self.name, self.city, self.country)

    def get_full_name(self):
        full_name = '%s %s' % (string.capitalize(self.user.first_name), string.capitalize(self.user.last_name))

        if len(full_name.lstrip()) == 0:
            return self.user.username

        return full_name
    full_name = property(get_full_name)

    def full_name_link(self, url_prefix=''):
        return '<a href="%s%s" class="user-profile">%s</a>' % (url_prefix, reverse('user_profile', args=[self.user.id]), self.full_name)

    def anonymous_name(self):
        if len(self.user.first_name) == 0 and len(self.user.last_name) == 0:
            return '%s %s' % (self.user.username[:3].capitalize(), self.user.username[:1].capitalize())
        else:
            return '%s %s' % (self.user.first_name, self.user.last_name[:1])

    def new_messages_count(self):
        if not hasattr(self, '_nmc'):
            self.get_messages_from()
        return ''

    def get_video_thumbnail(self):
        return VideoHelperFactory.get_helper(self.video_url).get_thumbnail_link()

    def get_video_embed_url(self):
        return VideoHelperFactory.get_helper(self.video_url).get_embed_url()


    @property
    def getShortLocation(self):
        if self.city and self.region:
            return "%s, %s" % (self.city, self.region)
        else:
            if self.city:
                return self.city
            else:
                return self.location_address

    @property
    def getLocation(self):
        """
        Long Location
        """
        if self.city and self.region and self.country:
            return "%s, %s, %s" % (self.city, self.region, self.country)
        else:
            if self.city and self.country:
                return "%s, %s" % (self.city,  self.country)

    @property
    def getCountry(self):
        """
        Full Country
        """
        result = ''
        if self.country:
            try:
                objCountry = Country.objects.get(code=self.country)
            except:
                pass
            else:
                result = objCountry.name
        return result


    @property
    def getAvatarImage(self):
        from multiuploader.models import MultiuploaderImage
        items = None
        try:
            userProfileObj = self
            items = MultiuploaderImage.objects.filter(userprofile=userProfileObj)
            if items:
                return items[0]
        except:
            pass
        return items

    @property
    def getActiveEventCount(self):
        """
        get count of active Event for the given User / provider
        """
        count = Event.objects.filter(author=self.user).count()
        return count

    @property
    def getAllEventCount(self):
        """
        get all Event which belong to the given User / provider
        """
        count = Event.objects.filter(author=self.user).count()
        return count

    @property
    def getNewMessagesCount(self):
        count = Message.objects.filter(archived='', recipient=self.user, read=False).exclude(origin__in=Message.MESSAGE_ALERT).count()
        return count

    @property
    def getArchivedMessagesCount(self):
        count = Message.objects.filter(archived='y', recipient=self.user, read=False).exclude(origin__in=Message.MESSAGE_ALERT).count()
        return count

    @property
    def getNewAlertsCount(self):
        count = Message.objects.filter(archived='', recipient=self.user, read=False, origin__in=Message.MESSAGE_ALERT).count()
        return count


class HelpQuestions(models.Model):
    question = models.CharField(max_length=255, unique=True)
    answer = models.TextField()

    def __unicode__(self):
        return "%s" % self.question

class ScheduledEmail(models.Model):
    to = models.ForeignKey(User, related_name='scheduled_emails')
    subject = models.CharField(max_length=255)
    body = models.TextField()
    plain_body = models.TextField()

class UserImageManager(models.Manager):
    """
    Custom manager for UserProfile images
    """
    def main_for_userprofile(self, userprofile_ids):
        """
        Select main image for each UserProfile in given list
        """
        return self.filter(userprofile__id__in=userprofile_ids)

class UserImageExtend(TimestampedModel, OrderableModelMixin):
    """
    Images For xauto profile (UserProfile)
    """
    userprofile = models.ForeignKey(UserProfile, related_name='userprofile_images')
    image = ImageWithThumbnailsField(upload_to='user_images/')
    caption = models.CharField(max_length=100, blank=True)
    objects = UserImageManager()


    def __unicode__(self):
        return self.image.name

    @property
    def url(self):
        return self.image.url

    def thumb_url(self, size):
        return unicode(self.image.extra_thumbnails.get(size))

    def copy_into(self, new_auction):
        from django.core.files.images import ImageFile

        new_obj = self._default_manager.create(
            userprofile=new_event,
            caption=self.caption,
            image=ImageFile(self.image))
        return new_obj

