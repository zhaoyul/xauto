from django.conf.urls import *
from django.views.generic.simple import direct_to_template
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from registration.views import activate
from views import register, UserProfileUpdateView,\
                  UserProfileCreateView, AccountUpdateView,\
                  AccountDeleteView
from forms import RegistrationForm, EmailAuthenticationForm

try:
    from django.core.urlresolvers import reverse_lazy
except ImportError, e:
    from django.core.urlresolvers import reverse
    from django.utils.functional import lazy
    reverse_lazy = lazy(reverse, str)


urlpatterns = patterns('',
           url(r'^activate/complete/$',
               direct_to_template,
               {'template': 'registration/activation_complete.html'},
               name='registration_activation_complete'),
           # Activation keys get matched by \w+ instead of the more specific
           # [a-fA-F0-9]{40} because a bad activation key should still get to the view;
           # that way it can return a sensible "invalid key" message instead of a
           # confusing 404.
           url(r'^activate/(?P<activation_key>\w+)/$',
               activate,
               {'backend': 'accounts.registration_backend.PhotoBackend'},
               name='registration_activate'),
           url(r'^register/$',
               register,
               {'backend': 'accounts.registration_backend.PhotoBackend',
                'form_class': RegistrationForm},
               name='registration_register'),
           url(r'^register/complete/$',
               direct_to_template,
               {'template': 'registration/registration_complete.html'},
               name='registration_complete'),
           url(r'^register/closed/$',
               direct_to_template,
               {'template': 'registration/registration_closed.html'},
               name='registration_disallowed'),
           url(r'^password/$',
               login_required(AccountUpdateView.as_view()),
               name='account_edit'),
           url('^(?P<pk>\d+)/delete/$',
               AccountDeleteView.as_view(),
               name="account_delete"),
           #url(r'^done/$', "accounts.views.fb_done", name='dsa_done'),
           #url(r'^error/$', "accounts.views.fb_error", name='dsa_error'),
           url('^profile/new',
               login_required(UserProfileCreateView.as_view()),
               name="profiles_create_profile"),
           url('^profile',
               login_required(UserProfileUpdateView.as_view()),
               name="profiles_edit_profile"),
           url(r'^login/$',
                auth_views.login,
                {'template_name': 'registration/login.html',
                'authentication_form': EmailAuthenticationForm,},
                name='auth_login'),
           (r'', include('registration.auth_urls')),
           )
