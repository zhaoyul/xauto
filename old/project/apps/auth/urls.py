from django.conf.urls import *
from django.views.generic import TemplateView
from registration.views import activate
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect


from auth.views import register  #, login, password_reset, resend_email
from auth.views import login, password_reset, resend_email
from views import welcome_xauto


def my_register(request, *args, **kwargs):
    if request.user.is_authenticated():
        return redirect('/')
    return register(request, *args, **kwargs)

urlpatterns = patterns('',
    url(r'^activate/complete/$', TemplateView.as_view(template_name="registration/activation_complete.html"), name='registration_activation_complete'),
    url(r'^register/complete/$', TemplateView.as_view(template_name="registration/registration_complete.html"), name='registration_complete'),
    url(r'^register/closed/$', TemplateView.as_view(template_name="registration/registration_closed.html"), name='registration_disallowed'),
    url(r'^activate/(?P<activation_key>\w+)/$', activate, {'backend': 'xauto.auth.backends.RegistrationBackend'}, name='registration_activate'),
    url(r'^register/$', my_register, {'backend': 'xauto.auth.backends.RegistrationBackend', 'success_url' : '/'}, name='registration_register'),
    url(r'^login/$', login, name='auth_login'),
    url(r'^welcome/$', welcome_xauto, name='welcome_xauto'),
    url(r'^activation/resend/$', resend_email, name='auth_resend_email'),
    url(r'^logout/$', auth_views.logout,  {'next_page': '/', }, name='auth_logout'),
    url(r'^password/reset/$', password_reset, name='auth_password_reset'), (r'', include('registration.auth_urls')),
)
