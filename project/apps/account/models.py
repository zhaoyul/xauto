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
from sorl.thumbnail.fields import ImageField
from autoslug import AutoSlugField

# ---------------------------------------------------
# --- Xauto Data models                           ---
# ---------------------------------------------------
from xauto_lib.models import TimestampedModel


class UserProfile(TimestampedModel):

    user = models.OneToOneField(User, related_name='profile')
    name = models.CharField(max_length=255, unique=True, default='')
    slug = AutoSlugField(populate_from='name',
        slugify=lambda value: value.replace(' ','-'))
    about = models.TextField(null=True, blank=True)

    location_address = models.CharField(max_length=255, null=True, blank=True)
    ip_location = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=30, null=True, blank=True)
    zipcode = models.CharField(max_length=10, null=True, blank=True)
    region = models.CharField(max_length=50, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    main_image = ImageField(upload_to='account_images/')
    thumbnail_image = ImageField(upload_to='account_images/')
    followed = models.ManyToManyField('account.UserProfile', null=True, blank=True,
        related_name='followed_profiles', verbose_name='Profile followed by')


    def get_full_name(self):
        full_name = '%s %s' % (string.capitalize(self.user.first_name),
                                string.capitalize(self.user.last_name))

        if len(full_name.lstrip()) == 0:
            return self.user.username

        return full_name
    full_name = property(get_full_name)
