from django.views.decorators.http import require_POST
from django.contrib.auth import login as auth_login
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.utils.importlib import import_module
from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login, logout as auth_logout
from registration.views import register as register_

from auth.backends import RegistrationBackend
from auth.forms import LoginForm, PasswordResetForm, HoneypotForm
from utils.ajax import json_view
from django.core.urlresolvers import reverse
from member.models import UserProfile
from livesettings import config_value

@require_POST
@csrf_protect
def register(request, *args, **kwargs):
    return register_(request, extra_context=dict({
        #'map_center': user_location(request),
        #'map_zoom': settings.DEFAULT_ZOOM,
        'invitation_key': request.GET.get('key', None)
    }, **kwargs.get('extra_context', {})), *args, **kwargs)


@require_POST
@csrf_protect
@json_view
def login(request, authentication_form=LoginForm):

    nextUrl = request.POST.get('return_url');
    form = authentication_form(data=request.POST)
    context = RequestContext(request)
    template = 'login_form.html'
    if 'is_join_login' in request.POST:
        template = 'join_login_form.html'
    
    is_main_form_valid = form.is_valid()
    honeypot_form = HoneypotForm(is_main_form_valid=is_main_form_valid, data=request.POST)
    context.update({'form': form, 'honeypot_form': honeypot_form})
    is_honeypot_form_valid = honeypot_form.is_valid()
    
    if is_honeypot_form_valid and is_main_form_valid:
        loginUser = form.get_user()
        auth_login(request, loginUser)
        
        # -----------------------------------------------------------------
        # ---- Get last Ip when Login and save it to UserProfile Table ----
        ip = request.META.get('HTTP_X_FORWARDED_FOR', '') or request.META.get('REMOTE_ADDR', '')
        ip = ip.split(',')[0].strip()
        if request.user:
            userprofileObj = UserProfile.objects.get(user=request.user)
            if userprofileObj:
                # ---- check if User active (not deleted not suspended) ---
                if not userprofileObj.is_deleted and not userprofileObj.is_suspended and not userprofileObj.is_closed:
                    userprofileObj.ip_location = ip
                    userprofileObj.save()
                    # ---- reset django session ---
                    request.session['distance'] = ''
                    request.session['latitude']  = ''
                    request.session['longitude'] = ''
                    request.session['location'] = ''
                    
                # --------------------------------------------
                # -- Inactive user (deleted or suspended)  ---
                else:
                    request.user.is_active = False
                    request.user.save()                    
                    reason = ''
                    if userprofileObj.is_deleted:
                        messageError = 'This user has been removed'
                    elif userprofileObj.is_closed:
                        messageError = 'This account has ben closed'
                    else:
                        messageError = 'This user has been suspended'
                        reason = userprofileObj.reason_suspended
                    context.update({
                        'error_login': messageError,
                        'reason': reason,
                    })
                    purgeUserSQession(request.user)
                    return render_to_response(template, context_instance=context)
        
        remember = request.POST.get('remember', False)
        login_days = config_value('SITE', 'LOGIN_DAYS')
        login_duration = remember and login_days * 60 * 60 * 24 or 0
        request.session.set_expiry(login_duration)
        if not nextUrl:
            return {'redirect_to': reverse('myxauto_current_activity')}
        else:
            return {'redirect_to': nextUrl}
    
    return render_to_response(template, context_instance=context)

@require_POST
@json_view
@csrf_protect
def password_reset(request,
        email_template_name='registration/password_reset_email.html',
        password_reset_form=PasswordResetForm,
        token_generator=default_token_generator):
    form = password_reset_form(request.POST)
    context = RequestContext(request)
    template = 'reset_password_form.html'
    if 'is_join_password_reset' in request.POST:
        template = 'join_reset_password_form.html'
    
    is_main_form_valid = form.is_valid()
    honeypot_form = HoneypotForm(is_main_form_valid=is_main_form_valid, data=request.POST)
    context.update({'form': form, 'honeypot_form': honeypot_form})
    is_honeypot_form_valid = honeypot_form.is_valid()
    if is_honeypot_form_valid and is_main_form_valid:
        opts = {}
        opts['use_https'] = request.is_secure()
        opts['token_generator'] = token_generator
        opts['email_template_name'] = email_template_name
        form.save(**opts)
        context.update({'reset_complete': '1'})
    
    return render_to_response(template, context_instance=context)

@json_view
@require_POST
def resend_email(request):
    email = request.POST.get('email', None)
    if email is None:
        email = request.POST.get('username', None)
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return {
            'status': 'error',
            'message': 'Couldn\'t find user with this email',
        }

    if user.is_active:
        return {
            'status': 'error',
            'message': 'User is active, just login',
        }

    RegistrationBackend().resend_email(user)
    return {
        'status': 'ok',
        'message': 'Activation email is sent, check your email',
    }


def purgeUserSQession(user):
    from django.contrib.sessions.models import Session
    from django.contrib.auth.models import User
    from django.http import HttpRequest
    from django.contrib.auth import logout
    from django.conf import settings
    from django.utils.importlib import import_module

    # grab the user in question 
    user = User.objects.get(pk=user.id)
    sessions = Session.objects.all()
    request = HttpRequest()
    
    for session in sessions:
        username = session.get_decoded().get('_auth_user_id')
        request.session = init_session(session.session_key)
        if username == user.id:
            logout(request)
            
def init_session(session_key):
    """
    Initialize same session as done for ``SessionMiddleware``.
    """
    from django.conf import settings
    from django.utils.importlib import import_module
    
    engine = import_module(settings.SESSION_ENGINE)
    return engine.SessionStore(session_key)     



def logout(request, next_page=None,
           template_name='registration/logged_out.html',
           redirect_field_name=REDIRECT_FIELD_NAME,
           current_app=None, extra_context=None):
    """
    Logs out the user and displays 'You are logged out' message.
    """
    auth_logout(request)
    redirect_to = request.REQUEST.get(redirect_field_name, '')
    if redirect_to:
        netloc = urlparse.urlparse(redirect_to)[1]
        # Security check -- don't allow redirection to a different host.
        if not (netloc and netloc != request.get_host()):
            return HttpResponseRedirect(redirect_to)

    if next_page is None:
        current_site = get_current_site(request)
        context = {
            'site': current_site,
            'site_name': current_site.name,
            'title': _('Logged out')
        }
        context.update(extra_context or {})
        return render_to_response(template_name, context,
                                  context_instance=RequestContext(request, current_app=current_app))
    else:
        # Redirect to this page until the session has been cleared.
        return HttpResponseRedirect(next_page or request.path)

        
