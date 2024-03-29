# ---------------------------------------------------
# --- Django base core code (system)              ---
# ---------------------------------------------------
from django.db import models
from django.contrib.auth.models import User

# ---------------------------------
# -- Various Python libraries   ---
# ---------------------------------
import string

# ---------------------------------------------------
# --- Django addon                                ---
# ---------------------------------------------------
from django_countries.fields import CountryField
from sorl.thumbnail.fields import ImageField
from autoslug import AutoSlugField
from sorl.thumbnail import get_thumbnail
from django.conf import settings

# ---------------------------------------------------
# --- Xauto Data models                           ---
# ---------------------------------------------------
from timezone_field import TimeZoneField
from xauto_lib.models import TimestampedModel


class UserProfile(TimestampedModel):

    user = models.OneToOneField(User, related_name='profile')
    slug = AutoSlugField(populate_from=lambda instance:instance.user.username,
                         always_update=True,
                         slugify=lambda value: value.replace(' ', '-'))
    about = models.TextField(null=True, blank=True)

    location_address = models.CharField(max_length=255, null=True, blank=True)
    ip_location = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=50,null=True, blank=True)
    country = CountryField(null=True, blank=True)
    zipcode = models.CharField(max_length=10, null=True, blank=True)
    region = models.CharField(max_length=50, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    timezone = TimeZoneField(null=False, blank=False, default='UTC')
    website = models.CharField(max_length=100, null=True, blank=True)

    main_image = ImageField(upload_to='account_images/', blank=True)
    thumbnail_image = ImageField(upload_to='account_images/', blank=True)
    followed = models.ManyToManyField('account.UserProfile', null=True, blank=True,
        related_name='followed_profiles', verbose_name='Profile followed by')
    activationtoken = models.CharField(max_length=255L,
        db_column='activationToken', null=True, blank=True)

    def get_full_name(self):
        full_name = self.user.get_full_name() or self.user.username
        return full_name

    full_name = property(get_full_name)

    def get_thumbnail(self, size, size2):
        if self.thumbnail_image:
            # TODO: refactor
            try:
                imgObject = get_thumbnail(self.thumbnail_image, str(size)+'x'+str(size2), crop='center', quality=99)
            except:
                return ""
            urlImg = imgObject.url
            return urlImg

    def get_main_image(self,size,size2):
        # TODO: refactor
        if self.main_image:
            try:
                imgObject = get_thumbnail(self.main_image, str(size)+'x'+str(size2), crop='center', quality=99)
            except:
                return ""
            urlImg = imgObject.url
            return urlImg
