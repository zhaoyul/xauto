import datetime

from django import forms
from django.forms.util import ErrorList
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, SetPasswordForm
from django.contrib.auth import authenticate
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.models import get_current_site
from django.template import Context, loader
from django.utils.translation import ugettext_lazy as _
from django.utils.http import int_to_base36
from django.utils.safestring import mark_safe

from auth.backends import RegistrationBackend
from auth.fields import HoneypotField, TimestampField
from utils.widgets import RoundedSelect, RoundedSplitDate
from utils.utils import geocode_place
from captcha.fields import CaptchaField, CaptchaTextInput


STATUS_CHOICES = (
    ('citizen','a citizen supporter'),
    ('leader','a leader of a campaign'),
    ('organization','a representative of an organization')
)

class HoneypotForm(forms.Form):
    phonenumber = HoneypotField(widget=forms.TextInput(attrs={'class': 'input'}),
                                label=_('Phone number'), required=False)
    timestamp = TimestampField()
    
    def __init__(self, is_main_form_valid=False, *args, **kwargs):
        super(HoneypotForm, self).__init__(*args, **kwargs)
        self.is_main_form_valid = is_main_form_valid
        if 'captcha_0' in self.data and 'captcha_1' in self.data:
            self._add_captcha_field()
    
    def _add_captcha_field(self):
        self.fields['captcha'] = CaptchaField(widget=CaptchaTextInput(attrs={'class': 'input captcha-input'}),
                                              error_messages={'invalid': _('Invalid CAPTCHA value.')})
    
    def clean(self):
        cleaned_data = self.cleaned_data
        if 'captcha' not in self.fields:
            if 'timestamp' in cleaned_data:
                fixed_delta = datetime.timedelta(seconds=3)
                timestamp, trying_count = cleaned_data['timestamp']
                delta = datetime.datetime.now() - timestamp
                if cleaned_data['phonenumber'] or delta < fixed_delta:
                    self._add_captcha_field()
                    raise forms.ValidationError(_('Anti-spam error.'))
                if trying_count >= 3 and not self.is_main_form_valid:
                    self._add_captcha_field()
                    raise forms.ValidationError(_('Anti-spam error.'))
            else:
                self._add_captcha_field()
                raise forms.ValidationError(_('Anti-spam error.'))
        return cleaned_data


class ResetPasswordForm(SetPasswordForm):
    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(_("Passwords did not match, please re enter."))
        return password2


class RegistrationForm(forms.Form):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'input'}), label="First Name")
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'input'}), label="Last Name")

    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'input'}), label="Email Address")

    password1 = forms.CharField(widget=forms.PasswordInput(render_value=True, attrs={'class': 'input'}),
                                label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput(render_value=True, attrs={'class': 'input'}),
                                label="Confirm Password")

    gender = forms.ChoiceField(choices=(
        ('', 'Choose'),
        ('M', 'Male'),
        ('F', 'Female'),
    ), label='GENDER', widget=RoundedSelect, required=False)

    birthdate = forms.DateField(widget=RoundedSplitDate(
        years=range(1930, datetime.date.today().year)),
        error_messages={
            'required': 'Birthdate is required',
        }, label='BIRTHDATE', required=False)

    tos = forms.BooleanField(label=mark_safe('I have read and agree with the <a href="%s">Terms of Use</a> & <a href="%s">Privacy Policy</a>' 
                                             % ('/terms-of-use', '/privacy-policy')),
                             error_messages={ 'required': "You must agree to register" })
    over18 = forms.BooleanField(label='I am over the age of 18 years',
                             error_messages={ 'required': "You must be 18 to register" })

    address = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'input'}), label="Your Location")
    latitude = forms.FloatField(widget=forms.HiddenInput, required=False)
    longitude = forms.FloatField(widget=forms.HiddenInput, required=False)
    city  = forms.CharField(widget=forms.HiddenInput, max_length=100, required=False, label="City Name")
    country  = forms.CharField(widget=forms.HiddenInput, max_length=100, required=False, label="Country Code")
    zipcode  = forms.CharField(widget=forms.HiddenInput, max_length=100, required=False, label="Postal Code")
    nexturl  = forms.CharField(widget=forms.HiddenInput, max_length=100, required=False, label="Next Url")

    def clean_email(self):
        try:
            User.objects.get(email=self.cleaned_data.get('email'))
        except User.DoesNotExist:
            return self.cleaned_data['email']
        raise forms.ValidationError(mark_safe('Account exists, please <a href="#" class="show-login-form">log in</a> here.'))

    def clean(self):
        # flow password validation through password1 field so template code only needs to show errors for password1
        if 'password1' not in self.cleaned_data or 'password2' not in self.cleaned_data or self.cleaned_data['password1'] != self.cleaned_data['password2']:
            if 'password1' not in self._errors:
                self._errors['password1'] = ErrorList('Passwords do not match')
        if 'first_name' in self.cleaned_data and ' ' in self.cleaned_data['first_name']:
            names = self.cleaned_data['first_name'].split(' ')
            self.cleaned_data['first_name'] = names[0]
            self.cleaned_data['last_name'] = ' '.join(names[1:])
            self._errors.pop('last_name')


        address = self.cleaned_data.get('address')
        #if address:
        #    place = geocode_place(address)
        #    if place:
        #        qs = self.cleaned_data['places'] or Place.objects.none()
        #        self.cleaned_data['places'] = qs | Place.objects.filter(id=place.id)
        return self.cleaned_data


class JoinForm(forms.Form):
    """
    Form for quick sign-up
    """
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'input'}), label="Name")

    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'input'}), label="Email Address")

    password1 = forms.CharField(widget=forms.PasswordInput(render_value=True, attrs={'class': 'input'}),
                                label="Password")

    tos = forms.BooleanField(label=mark_safe('I am over 18, I have read and agree with the <a href="%s">Terms of Use</a> & <a href="%s">Privacy Policy</a>' 
                                             % ('/terms-of-use', '/privacy-policy')),
                             error_messages={ 'required': "You must agree to register" })
    
    address  = forms.CharField(widget=forms.HiddenInput, max_length=100, required=False, label="Your Location")
    latitude = forms.FloatField(widget=forms.HiddenInput, required=False)
    longitude = forms.FloatField(widget=forms.HiddenInput, required=False)
    nexturl  = forms.CharField(widget=forms.HiddenInput, max_length=100, required=False, label="Next Url")

    def clean_email(self):
        try:
            User.objects.get(email=self.cleaned_data.get('email'))
        except User.DoesNotExist:
            return self.cleaned_data['email']
        raise forms.ValidationError(mark_safe('Account exists, please <a href="#" class="show-join-login-form">log in</a> here.'))

    def clean(self):
        if 'name' in self.cleaned_data:
            if ' ' in self.cleaned_data['name']:
                names = self.cleaned_data['name'].split(' ')
                self.cleaned_data['first_name'] = names[0]
                self.cleaned_data['last_name'] = ' '.join(names[1:])
            else:
                self.cleaned_data['first_name'] = self.cleaned_data['name']
                self.cleaned_data['last_name'] = ''
        return self.cleaned_data


class LoginForm(AuthenticationForm):
    messages = {
        'wrong': 'Please enter a correct username and password.<br /> Note that both fields are case-sensitive.',
        'deactivated': 'This account is deactivated.',
        'inactive': 'Your account has not been activated yet. An email has been sent to you. Simply click on the link in the email to activate your email.',
        'cookies': 'Your Web browser doesn\'t appear to have cookies enabled. Cookies are required for logging in.',
    }
    username = forms.CharField(label="Username", max_length=200, widget=forms.TextInput(attrs={'class': 'input'}))
    password = forms.CharField(widget=forms.PasswordInput(render_value=True, attrs={'class': 'input'}),
                                label="Password")
    remember = forms.BooleanField(required=False)
    return_url = forms.CharField(widget=forms.HiddenInput, required=False)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            self.user_cache = authenticate(username=username, password=password)
            if self.user_cache is None:
                try:
                    user = User.objects.get(email=username)
                except User.DoesNotExist:
                    pass
                else:
                    if not user.is_active:
                        raise forms.ValidationError(self.messages['inactive'])
                raise forms.ValidationError(mark_safe(self.messages['wrong']))

        # TODO: determine whether this should move to its own method.
        if self.request:
            if not self.request.session.test_cookie_worked():
                raise forms.ValidationError(self.messages['cookies'])

        return self.cleaned_data


class PasswordResetForm(forms.Form):
    email = forms.EmailField(label=_("E-mail"),
                             error_messages={'invalid': _("Email invalid please try again.")},
                             widget=forms.TextInput(attrs={'class': 'input', 'id': 'id_email_reset'}),
                             max_length=75)

    def clean_email(self):
        """
        Validates that an active user exists with the given e-mail address.
        """
        email = self.cleaned_data["email"]
        self.users_cache = User.objects.filter(email__iexact=email)
        if len(self.users_cache) == 0:
            raise forms.ValidationError(_("Account not found, please try again."))
        return email

    def save(self, domain_override=None, email_template_name='registration/password_reset_email.html',
             use_https=False, token_generator=default_token_generator, from_email=None, request=None):
        """
        Generates a one-use only link for resetting password and sends to the user
        """
        from django.core.mail import send_mail
        for user in self.users_cache:
            if not domain_override:
                current_site = get_current_site(request)
                site_name = current_site.name
                domain = current_site.domain
            else:
                site_name = domain = domain_override
            t = loader.get_template(email_template_name)
            c = {
                'email': user.email,
                'domain': domain,
                'site_name': site_name,
                'uid': int_to_base36(user.id),
                'user': user,
                'token': token_generator.make_token(user),
                'protocol': use_https and 'https' or 'http',
            }
            send_mail(_("Password reset on %s") % site_name,
                t.render(Context(c)), from_email, [user.email])
