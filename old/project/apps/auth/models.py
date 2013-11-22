from django.db import models
from django.contrib.auth.models import User


class RegistrationRedirect(models.Model):
    user = models.OneToOneField(User, related_name='registration_redirect')
    redirect = models.CharField(max_length=200)
