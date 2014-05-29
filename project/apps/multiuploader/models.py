from django.db import models
import random
from sorl.thumbnail import get_thumbnail
from django_resized.forms import ResizedImageField
from django.contrib.auth.models import User

from account.models import UserProfile

from django.conf import settings
from xauto_lib.models import TimestampedModel

try:
    storage = settings.MULTI_IMAGES_FOLDER + '/'
except AttributeError:
    storage = 'multiuploader_images/'


class MultiuploaderImage(TimestampedModel):
    """
    Model for storing uploaded photos for User Profile Table and Event Table
    """
    IMAGE_TYPE = (
        ('team', 'team'),
        ('event', 'event'),
        ('user', 'user'))

    userprofile = models.ForeignKey(UserProfile, blank=True, null=True,
                                    related_name='profile_images')
    event_date = models.ForeignKey('event.EventDate', blank=True, null=True,
                                   related_name='event_upload_images')
    filename = models.CharField(max_length=60, blank=True, null=True)
    about = models.CharField(max_length=255, blank=True, null=True)
    key_data = models.CharField(max_length=90, unique=True, blank=True,
                                null=True)
    image_type = models.CharField(max_length=10, blank=True, null=True)
    size = models.FloatField(default=0.0)
    upload_date = models.DateTimeField(auto_now_add=True)
    application = models.CharField(choices=IMAGE_TYPE, max_length=30,
                                   default='team')
    latitude = models.FloatField(default=0.00)
    longitude = models.FloatField(default=0.00)
    is_irrelevant = models.BooleanField(default=False)
    is_inappropriate = models.BooleanField(default=False)
    favorite_by = models.ManyToManyField(UserProfile,
                                         related_name='favorite_images', null=True, blank=True,
                                         verbose_name='Image favorite by')

    image = ResizedImageField(max_width=1600, max_height=1200, upload_to=storage)
    caption = models.CharField(max_length=100, blank=True)

    @property
    def key_generate(self):
        """returns a string based unique key with length 80 chars"""
        while 1:
            key = str(random.getrandbits(256))
            try:
                MultiuploaderImage.objects.get(key=key)
            except:
                return key

    def __unicode__(self):
        return self.image.name

    @property
    def url(self):
        return self.image.url

    def get_thumb(self, size):
        try:
            img = get_thumbnail(self.image,
                                size,
                                crop='center',
                                quality=99)
            return img.url
        except IOError:
            pass
        return self.image.url

    def thumb_url(self):
        return self.get_thumb(settings.THUMBNAIL_SIZE)

    def photoviewer_url(self, size):
        return self.get_thumb(settings.PHOTOVIEWER_SIZE)


class MultiuploaderFiles(TimestampedModel):
    """
    Model for storing uploaded files (any usage)
    """

    IMAGE_TYPE = (
        ('team', 'team'),
        ('event', 'event'),
        ('message', 'message'),
        ('user', 'user'))

    user = models.ForeignKey(User, blank=True, null=True,
                             related_name='upload_files')
    event_date = models.ForeignKey('event.EventDate', blank=True, null=True,
                                   related_name='event_upload_files')
    filename = models.CharField(max_length=60, blank=True, null=True)
    file_type = models.CharField(max_length=10, blank=True, null=True)
    path = models.CharField(max_length=255, blank=True, null=True)
    key_data = models.CharField(max_length=90, unique=True, blank=True,
                                null=True)
    size = models.FloatField(default=0.0)
    upload_date = models.DateTimeField(auto_now_add=True)
    application = models.CharField(choices=IMAGE_TYPE, max_length=30,
                                   default='team')
    caption = models.CharField(max_length=100, blank=True)

    def __unicode__(self):
        return self.filename

    @property
    def url(self):
        return '/media/%s' % self.path

    @property
    def key_generate(self):
        """returns a string based unique key with length 80 chars"""
        while 1:
            key = str(random.getrandbits(256))
            try:
                MultiuploaderFiles.objects.get(key=key)
            except:
                return key



