from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.dispatch import receiver
from registration.signals import user_activated

#class UserProfile(models.Model):
#    user = models.ForeignKey(User, unique=True)

#User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])

# force emails to be uniqe
User._meta.get_field_by_name('email')[0]._unique = True

#http://djangosnippets.org/snippets/1960/
@receiver(user_activated)
def login_on_activation(sender, user, request, **kwargs):
    """Automatically login a user after activation
    """
    user.backend='accounts.auth_backends.EmailAuthBackend'
    login(request, user)

# When model instance is saved, trigger creation of corresponding profile
#@receiver(post_save, sender=User)
#def create_profile(sender, instance, signal, created, **kwargs):
#    """When user is created also create a matching profile."""
#    if created:
#        UserProfile(user = instance).save()
