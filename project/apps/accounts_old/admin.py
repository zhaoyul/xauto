from django.contrib import admin
from django.contrib.auth.models import User

from reversion.helpers import patch_admin
from reversion.admin import VersionAdmin
#from accounts.models import UserProfile

#patch_admin(User)

#class UserProfileAdmin(VersionAdmin):
#    """Admin settings go here."""

#admin.site.register(UserProfile, UserProfileAdmin)
