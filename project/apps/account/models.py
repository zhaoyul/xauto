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
from sorl.thumbnail import get_thumbnail
from project import settings

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
    state = models.CharField(max_length=50,null=True, blank=True)
    country = models.CharField(max_length=30, null=True, blank=True)
    zipcode = models.CharField(max_length=10, null=True, blank=True)
    region = models.CharField(max_length=50, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    main_image = ImageField(upload_to='account_images/', blank=True)
    thumbnail_image = ImageField(upload_to='account_images/', blank=True)
    followed = models.ManyToManyField('account.UserProfile', null=True, blank=True,
        related_name='followed_profiles', verbose_name='Profile followed by')
    activationtoken = models.CharField(max_length=255L,
        db_column='activationToken', null=True, blank=True)


    def get_full_name(self):
        full_name = '%s %s' % (string.capitalize(self.user.first_name),
                                string.capitalize(self.user.last_name))

        if len(full_name.lstrip()) == 0:
            return self.user.username

        return full_name
    full_name = property(get_full_name)

    def get_thumbnail(self,size,size2):
        if self.thumbnail_image:
            root =  "/".join(settings.MEDIA_ROOT.split('/')[0:-1])
            try:
                imgObject = get_thumbnail(root + self.thumbnail_image.url, str(size)+'x'+str(size2), crop='center', quality=99)
            except:
                return ""
            urlImg = imgObject.url
            return urlImg

    def get_main_image(self,size,size2):
        if self.main_image:
            root =  "/".join(settings.MEDIA_ROOT.split('/')[0:-1])
            try:
                imgObject = get_thumbnail(root + self.main_image.url, str(size)+'x'+str(size2), crop='center', quality=99)
            except:
                return ""
            urlImg = imgObject.url
            return urlImg
