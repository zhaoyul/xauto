import random

from django import forms
from django.contrib.auth import login
from django.contrib.auth.backends import ModelBackend
from django.core.validators import email_re
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.utils.hashcompat import sha_constructor
from django.conf import settings
from django.template import RequestContext
from django.shortcuts import render_to_response


from utils import log
from auth.tasks import sendXautoEmails
from member.models import UserProfile, userLanguage
from event.models import Currency
from utils.email import django_send_mail

from registration.backends.default import DefaultBackend
from registration.models import RegistrationProfile

from auth.models import RegistrationRedirect
from utils.email import render_subject_message
from utils.email import django_send_mail


def generate_username(email):
    salt = sha_constructor(str(random.random())).hexdigest()[:5]
    return sha_constructor(email + salt).hexdigest()[:30]






class RegistrationBackend(DefaultBackend):
    """
    Fills `username` with generated value (to use email for login),
    creates `profile` of needed type.
    """

    def get_form_class(self, request):
        from xauto.auth.forms import RegistrationForm, JoinForm
        form_class = RegistrationForm
        if 'is_join' in request.POST:
            form_class = JoinForm
        class Form(form_class):
            next = forms.CharField(max_length=200,
                                   widget=forms.HiddenInput,
                                   required=False,
                                   initial=request.REQUEST.get('next'))
        return Form

    def register(self, request, **kwargs):
        username, email, password = generate_username(kwargs['email']), kwargs['email'], kwargs['password1']

        nextUrl = kwargs.get('nexturl')
        user = User.objects.create_user(email, email, password)
        location = kwargs.get('address')
        city = kwargs.get('city')
        country = kwargs.get('country')
        zipcode = kwargs.get('zipcode')
        user.is_active = False
        user.first_name = kwargs['first_name']
        user.last_name = kwargs['last_name']
        currency_code = None
        defaultCountry = settings.DEFAULT_COUNTRY
        user.save()
        
        localLatitude  = kwargs['latitude']
        localLongitutde = kwargs['longitude']
        defaultlanguage = settings.LANGUAGE_CODE
        langObject  = userLanguage.objects.get(code=defaultlanguage)
        
        # ------------------------------------
        # ---- get user IP when Sign Up ------
        ip = request.META.get('HTTP_X_FORWARDED_FOR', '') or \
             request.META.get('REMOTE_ADDR', '')
        ip = ip.split(',')[0].strip()
        
        # -------------------------------------
        # --- Get currency                  ---
        currencyObject = Currency.objects.filter(country_code=country)
        if currencyObject:
            currency_code = currencyObject[0]
        else:
            currencyObject = Currency.objects.filter(country_code=defaultCountry)
            if currencyObject:
                currency_code = currencyObject[0]
            
        
        # ------------------------------------------------
        # --- register User Profile Data               --- 
        UserProfile.objects.create(user=user,
            location_address= location,
            city= city,
            country= country,
            currency=currency_code,
            zipcode= zipcode,
            name=kwargs['last_name'],
            latitude=localLatitude,
            longitude=localLongitutde,
            language=langObject,
            ip_location = ip
            )  
        
        if 'next' in kwargs or nextUrl:
            if nextUrl:
                redirectUrl  =nextUrl
            else:
                redirectUrl = kwargs['next']
            RegistrationRedirect.objects.create(user=user, redirect=redirectUrl)

        registration_profile = RegistrationProfile.objects.create_profile(user)
        self.send_activation_email(registration_profile)
        return user

    def activate(self, request, *args, **kwargs):
        user = super(RegistrationBackend, self).activate(request, *args, **kwargs)
        if user:
            user.backend='django.contrib.auth.backends.ModelBackend'
            login(request, user)
        return user

    def post_registration_redirect(self, request, user):
        template_name = 'registration/registration_form.html'
        context = RequestContext(request)
        return render_to_response(template_name,  { 'register_complete': '1' , 'newuser' : user  }, context_instance=context)

    def post_activation_redirect(self, request, user):
        try:
            if user.registration_redirect.redirect:
                return (user.registration_redirect.redirect, (), {})
        except:
            pass
        return ('/#activation-complete', (), {})

    def resend_email(self, user):
        RegistrationProfile.objects.filter(user=user).delete()
        profile = RegistrationProfile.objects.create_profile(user)
        self.send_activation_email(profile)
        return profile

    def send_activation_email(self, profile):
        subject, message = render_subject_message(
            'registration/activation_email_subject.txt',
            'registration/activation_email.txt', {
                'activation_key': profile.activation_key,
                'user': profile.user,
                'expiration_days': settings.ACCOUNT_ACTIVATION_DAYS,
            })

        #profile.user.email_user(subject, message, settings.DEFAULT_FROM_EMAIL)
        emailTo = []
        emailToString = profile.user.email
        emailTo.append(emailToString)
        log.tofile('send_mail', 'email [%s] sent to %s' % (subject, emailTo))
        django_send_mail(subject, message, emailTo, from_email=settings.DEFAULT_FROM_EMAIL)
        

class EmailBackend(ModelBackend):
    """
    Authenticates based on email instead of name.
    """
    def authenticate(self, username=None, password=None):
        if email_re.search(username):
            try:
                user = User.objects.get(email=username, is_active=True)
                if user.check_password(password):
                    return user
            except User.DoesNotExist:
                return None
        return None

    def get_user(self, user_id):
        try:
            return User.objects.select_related('profile', 'leader_profile').get(pk=user_id)
        except User.DoesNotExist:
            return None