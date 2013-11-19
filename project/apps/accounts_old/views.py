from random import choice
from string import letters
from django.shortcuts import redirect, render_to_response, get_object_or_404
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.messages.api import get_messages
from django.views.generic import UpdateView, CreateView,\
                                 TemplateView, DeleteView
from django.utils.translation import ugettext as _
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from registration.backends import get_backend
from accounts.forms import ProfileForm, AccountForm

def register(request, backend, success_url=None, form_class=None,
             disallowed_url='registration_disallowed',
             template_name='registration/registration_form.html',
             extra_context=None):

    backend = get_backend(backend)
    if not backend.registration_allowed(request):
        return redirect(disallowed_url)
    if form_class is None:
        form_class = backend.get_form_class(request)

    if request.method == 'POST':
        data = request.POST.copy() # so we can manipulate data
        form = form_class(data, files=request.FILES)
        if form.is_valid():
            # random username
            form.cleaned_data['username'] = ''.join([choice(letters) for i in xrange(30)])
            new_user = backend.register(request, **form.cleaned_data)
            if success_url is None:
                to, args, kwargs = backend.post_registration_redirect(request, new_user)
                return redirect(to, *args, **kwargs)
            else:
                return redirect(success_url)
    else:
        form = form_class()

    if extra_context is None:
        extra_context = {}
    context = RequestContext(request)
    for key, value in extra_context.items():
        context[key] = callable(value) and value() or value

    return render_to_response(template_name,
                              {'form': form},
                              context_instance=context)


class AccountUpdateView(UpdateView):
    template_name='accounts/account_change_form.html'
    form_class = AccountForm

    def get_success_url(self):
        messages.success(self.request, _('Account changed!'))
        return reverse('account_edit')

    def get_object(self, queryset=None):
        return get_object_or_404(User, pk=self.request.user.pk)

class AccountDeleteView(DeleteView):
    model = User
    template_name='accounts/account_confirm_delete.html'
    context_object_name='account'
    success_url = '/'

    def get_queryset(self):
        return User.objects.filter(pk=self.request.user.pk)

    def get_success_url(self):
        messages.success(self.request, _('User account removed!'))
        return '/'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(AccountDeleteView, self).dispatch(*args, **kwargs)


class UserProfileCreateView(CreateView):
    template_name = 'profiles/create_profile.html'
    #model = UserProfile
    
    def dispatch(self, request, *args, **kwargs):
        try:
            profile_obj = request.user.get_profile()
            return HttpResponseRedirect(reverse('profiles_edit_profile'))
        except ObjectDoesNotExist:
            pass
        return super(UserProfileCreateView, self).dispatch(request, *args, **kwargs)

    def get_form(self, form_class):
        """
        Returns an instance of the form to be used in this view.
        """
        kwargs = self.get_form_kwargs()
        kwargs['initial'].update({'email':self.request.user.email})
        return form_class(**kwargs) 

    def get_success_url(self):
        return reverse('profiles_edit_profile')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        messages.success(self.request, _('User Profile added!'))
        return HttpResponseRedirect(self.get_success_url())

    def get_form_class(self):
        return ProfileForm


class UserProfileUpdateView(UpdateView):
    template_name = 'profiles/edit_profile.html'
    #model = UserProfile
    
    def dispatch(self, request, *args, **kwargs):
        try:
            profile_obj = request.user.get_profile()
        except ObjectDoesNotExist:
            return HttpResponseRedirect(reverse('profiles_create_profile'))
        kwargs['pk'] = profile_obj.pk 
        return super(UserProfileUpdateView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('profiles_edit_profile')

    def form_valid(self, form):
        messages.success(self.request, _('User Profile changed!'))
        return super(UserProfileUpdateView, self).form_valid(form)

    def get_form_class(self):
        return ProfileForm


