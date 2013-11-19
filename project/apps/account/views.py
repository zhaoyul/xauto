from xauto_lib.views import BaseView, AdaptiveMixin
from xauto_lib.utils import flatten_errors, parsString, getAdminUser
from xauto_lib.decorators import json_view, post_required
from django.db.models import Avg, Count, Q, Sum, Max

from account.forms import AccountForm, PasswordForm, ServiceProfileEditForm, CustomerProfileEditForm, AlertForm, AlertSystemForm
from member.models import  Message, FeedbackRating, UserImageExtend, UserProfile, Feedback
from event.models import  Event
from multiuploader.models import MultiuploaderImage
from keywords.models import KeywordService, UserKeywordService
from account.models import AlertAd, AlertSystem
from xauto_lib.calutil import getDateRangeStamp
from xauto_lib.utils import send_email
from keywords.models import UserKeywordService
from xauto_lib.utils import CheckNumeric, getSystemParameters
from bidselect.views import SendMessage
from account.models import Parameters


from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, Http404
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.views.generic import TemplateView
from django.views.generic.edit import BaseUpdateView
from django.views.decorators.cache import cache_control
from django.template import RequestContext
from django.conf import settings
from django.core.files.uploadedfile import UploadedFile
from django.views.decorators.cache import cache_page, never_cache
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core.context_processors import csrf

from livesettings import config_value, config_register
import datetime, string


def myaccount(request):
    """
    xauto Myaccount  page. (new or current design) Layout 2012
    """

    template_name = 'myaccount.html'
    ctx =  {
        'member': None,
        'main_section': 'myaccount',
        }
    html = render_to_string(template_name, ctx, context_instance=RequestContext(request))
    return HttpResponse(html)



def testimonial(request, *args, **kwargs):
    """
    xauto Myaccount  page. (new or current design) Layout 2012
    """

    customer_id = kwargs.pop('customer_id')
    origin = kwargs.pop('origin', None)
    editProfile = request.GET.get('edit_profile', '')
    userMessage = request.GET.get('message', '')

    customer = get_object_or_404(User, pk=customer_id)
    customerProfile = UserProfile.objects.filter(user=customer)
    customerObj = None
    if customerProfile:
        customerObj = customerProfile[0]

    # ----------------------------------
    # ---- get 'Comments Received' -----
    comments = []

    template_name = 'account/page-testimonials.html'
    ctx =  {
        'customer' : customerObj,
        'customer_profile': 'y',
        'main_section': 'testimonial',
        'edit_profile': '',
        'preview' : 'y',
        'edit': editProfile,
        'comments': comments,
        'origin': origin
        }
    html = render_to_string(template_name, ctx, context_instance=RequestContext(request))
    return HttpResponse(html)



class BaseSettingsView(AdaptiveMixin, BaseUpdateView, TemplateView, BaseView):
    """
    Base class for account settings views.
    """
    method_names = ['GET', 'POST']
    valid_responses = {
        'GET': ['html'],
        'POST': ['json'],
    }
    success_url = '.'

    def get_object(self):
        return self.request.user

    def get_user_image(self):
        items = []
        try:
            userProfileObj = self.get_profile()[0]
            items = MultiuploaderImage.objects.filter(userprofile=userProfileObj, application='user')
        except:
            pass
        return items

    def get_profile(self):
        userProfile = UserProfile.objects.filter(user=self.request.user)
        return userProfile


    def form_valid(self, *form, **forms):
        if self.request.is_ajax():
            return self.render_to_response({
                'message': "Your contact details have been saved.",
            })
        else:
            return self.render_to_response(self.get_context_data(
                account_form=forms['account_form'], password_form=forms['password_form']))

    def form_invalid(self, *form, **forms):
        if len(form):
            forms = {'form': form[0]}

        if self.request.is_ajax():
            errors = {}
            for form in forms.values():
                errors.update(form.errors)
            ctx = {
                'result': 'error',
                'errors': flatten_errors(errors),
                'geocoding': geocoding,
            }
            return self.render_to_response(ctx)
        else:
            return self.render_to_response(forms)

    def get_context_data(self, *args, **kwargs):
        context = super(BaseSettingsView, self).get_context_data(*args, **kwargs)
        context['view_name'] = self.view_name
        return context

class AccountView(BaseSettingsView):
    template_name = 'account/page-account-details.html'
    form_class = AccountForm
    view_name = 'account'

    def get(self, request, *args, **kwargs):

        reasonListSelector = getSystemParameters(Parameters.REPORT, Parameters.CLOSE_ACCOUNT, mode='')

        mode = request.GET.get('mode', 'view')
        self.object = self.get_object()
        self.profile = self.get_profile()
        if mode == 'edit':
            self.template_name = 'account/page-account-details-edit.html'
        account_form = AccountForm(instance=self.object, mode=mode)
        password_form = PasswordForm(member=self.object)
        currentContext = self.get_context_data(account_form=account_form, password_form=password_form)
        currentContext['geocoding'] = "y"
        currentContext['account_detail'] = "y"
        currentContext['member'] = self.profile
        currentContext['close_reason'] = reasonListSelector
        return self.render_to_response(currentContext)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.profile = self.get_profile()
        mode = request.POST.get('mode_account', 'view')
        reasonListSelector = getSystemParameters(Parameters.REPORT, Parameters.CLOSE_ACCOUNT, mode='')

        # ---------------------------------------------------------------------
        # ---- during edit process loop on myaccount_dedit                -----
        # ---- currently after save we loop on origin view Mode if save ok ----
        if mode == 'edit':
            self.template_name = 'account/page-account-details-edit.html'
        account_form = AccountForm(
            self.request.POST,
            instance=self.object,
            mode=mode
        )
        password_form = PasswordForm(
            self.request.POST,
            member=self.object,
        )
        if account_form.is_valid() and password_form.is_valid():
            account_form.save()
            password_form.save()
            currentContext = self.get_context_data(account_form=account_form, password_form=password_form)
            currentContext['message'] = "Your account details have been saved"
            currentContext['geocoding'] = "y"
            currentContext['member'] = self.profile
            currentContext['close_reason'] = reasonListSelector
            self.template_name = 'account/page-account-details.html'   # -- return to view mode --
            return self.render_to_response(currentContext)

        # ------------------------------------
        # ---- errors have been detected ------
        else:
            currentContext = self.get_context_data(account_form=account_form, password_form=password_form)
            currentContext['message'] = "Opps, please check errors below"
            currentContext['errors'] = "Y"
            currentContext['geocoding'] = "y"
            currentContext['member'] = self.profile
            currentContext['close_reason'] = reasonListSelector
            return self.render_to_response(currentContext)

class CustomerProfileEditView(BaseSettingsView):
    """
    Customer Profile Edit Page
    """

    template_name = 'account/page-customer-profile-edit.html'
    form_class = AccountForm
    view_name = 'customer_profile_view'

    def get(self, request, *args, **kwargs):
        mode = request.GET.get('mode', 'view')
        self.object = self.get_object()
        account_form = AccountForm(instance=self.object, mode=mode)
        return self.render_to_response(self.get_context_data(
            account_form=account_form))

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        mode = request.POST.get('mode_view', 'view')

        # ---------------------------------------------------------------------
        # ---- during edit process loop on Customer  Profile Edit          ----
        # ---- currently after save we loop on origin view Mode if save ok ----
        account_form = AccountForm(
            self.request.POST,
            instance=self.object,
        )

        if account_form.is_valid() :
            account_form.save()
            currentContext = self.get_context_data(account_form=account_form, password_form=password_form)
            currentContext['message'] = "Your account details have been saved"
            self.template_name = 'account/page-customer-profile-edit.html'   # -- return to view mode --
            return self.render_to_response(currentContext)
        else:
            return self.form_invalid(account_form=account_form)


# ---------------------------------------------------------
# ---------------------------------------------------------
# ---- Account xauto Image processing for UerProfile
# ---------------------------------------------------------
# ---------------------------------------------------------

# Temporary
from django import forms
class UserProfilerImageForm(forms.ModelForm):
    class Meta:
        model = UserImageExtend
        fields = ('image',)

    def __init__(self, *args, **kwargs):
        super(UserProfilerImageForm, self).__init__(*args, **kwargs)
        self.instance.userprofile = kwargs['initial']['userprofile']


class UserProfileImagesView(BaseView):
    """
    Handle querying, adding, removing and reordering xauto profile  images.
    """
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        response = self.get_images(request)
        return self.render_to_response(response)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        action = request.POST['action']
        if action == 'add':
            response = self.add_image(request)
        elif action == 'remove':
            response = self.remove_image(request)
        elif action == 'reorder':
            response = self.reorder_images(request)
        return self.render_to_response(response, force_ajax=True)

    def get_images(self, request):
        "Return list of user profile  images."
        qs = self.object.images.all()
        main = qs and qs[0] or None

        response = {
            'images': [{
                'id': image.id,
                'url': image.thumb_url('small'),
            } for image in qs]
        }
        if qs:
            response['main'] = {
                'id': qs[0].id,
                'url': qs[0].thumb_url('medium'),
            }
        return response

    def add_image(self, request):
        "Add a image to the user profile ."
        form = UserProfilerImageForm(request.POST, request.FILES,
            initial={'userprofile': self.object})
        if form.is_valid():
            new_image = form.save()
            response = {
                'id': new_image.id,
                'url': new_image.thumb_url('preview'),
            }
            if new_image == self.object.main_image:
                response['main_url'] = new_image.thumb_url('medium')
            return response

        else:
            return {
                'result': 'error',
                'errors': flatten_errors(form.errors),
            }

    def remove_image(self, request):
        "Remove a image from the userprofile ."
        image_id = request.POST['id']
        result = {}
        try:
            self.object.images.get(id=image_id).delete()
            result['removed'] = image_id
            result['status'] = 'ok'
        except UserImageExtend.DoesNotExist:
            result['removed'] = None
            result['status'] = 'error'
            return result
        return result

    def reorder_images(self, request):
        "Change userprofile images ordering."
        images = dict([(str(a.id), a) for a in self.object.images.all()])
        ids = request.POST.getlist('ids[]')
        for id in ids:
            images[id].order = 0
            images[id].save()
        return self.get_images(request)


@never_cache
@login_required
@json_view
def user_list_image(request, user, mode='account', application='user'):
    """
    Return list of images related to member/user.

    """
    user_mode = mode
    application_extra = request.GET.get('application')
    if application_extra:
        application = application_extra

    # -------------------------------------------
    # -- get extrat Get or Post parameters    ---
    try:
        user_mode = request.GET.get('mode')
        if user_mode:
            mode = user_mode
    except:
        try:
            user_mode = request.POST.get('mode')
            if user_mode:
                mode = user_mode
        except:
            pass


    # --------------------------------
    # --- Target Html form         ---
    if mode == 'account':
        template_name = 'account/block-images.html'
    else:
        template_name = 'account/block-images-manage.html'

    # ----------------------------------------------------
    # --- extract all Images for the selected member -----
    imageList = MultiuploaderImage.objects.filter(userprofile=user, application=application)

    # ----------------------------------
    # ---- prepare Html rendering ------
    ctx = {
        'items': imageList,
        'ajax': True,
        'total_count': imageList.count(),
    }

    # -------------------------------------------
    # --- Html rendering                      ---
    html = render_to_string(template_name, ctx, context_instance=RequestContext(request))
    return {
        "html": html,
        "total_count": imageList.count(),
    }

@login_required
@json_view
def user_get_avatar(request, user, application='user'):
    """
    Return User's avatar.
    """

    template_name = 'account/block-images-avatar.html'
    imageList = MultiuploaderImage.objects.filter(userprofile=user, application=application)[:1]
    ctx = {'items': imageList, }
    html = render_to_string(template_name, ctx, context_instance=RequestContext(request))
    return { "html": html,  }


@login_required
@json_view
def add_keyword(request, user):
    """
    add a new Keyword to Userprofile
    UserprofileOb = UserProfile.objects.filter()   // get Userprofile record Object/Id
    KeywordsObj = KeywordService.objects.filter()  // get keyword record Object/Id
    UserprofileOb.keywords.add(KeywordsObj)        // add to M2M table the new keywords for the current User
    ====> We can several Keywords add the same time add(ccc, gggg)
    UserprofileOb.save()                           // finally save the Current Userprofile record
    """

    status = "ok"
    msg_error = ""
    ctrNewKeyword = 0
    keywordObj = None
    keywordList = []
    userKeywordList = []
    nbrKeywords = 0
    nbrUserKeywords = 0
    customerUserKeyword = False
    currentUser = request.user
    addExistingUserKeyword = False
    template_name = 'account/block-keywords.html'
    keyword = request.POST.get('keyword')
    keyword_id = request.POST.get('id')
    keyword_custom = request.POST.get('custom', '')

    # ---------------------------------------
    # -- user has filled a custom Keyword ---
    # ---------------------------------------
    if keyword_custom:
        keyword = keyword_custom
        customerUserKeyword = True

    # -------------------------------------------------------
    # ---- get handle of the current User profile record ----
    # -------------------------------------------------------
    userProfileObject =   UserProfile.objects.filter(id=user)
    if userProfileObject:
        userObj = userProfileObject[0]

    # -----------------------------------------------------------------
    # -----------------------------------------------------------------
    # ---  S T A N D A R D          K E Y W O R D S                ----
    # ---  check if the keyword already added to this user profile ----
    # --- only for Builtin Keywords                                ----
    # -----------------------------------------------------------------
    # -----------------------------------------------------------------
    if not customerUserKeyword and userObj:
        # ----------------------------------------------------------------------------------
        # --- check if this keyword is already attached to the current User profile      ---
        # ----------------------------------------------------------------------------------
        CheckKeywordObj  = UserProfile.objects.filter(keywords__keyword=keyword, user=userObj.user)
        if CheckKeywordObj:
            status ="error"
            msg_error = "Keyword already added"

        # ----------------------------------------------------------------------------------
        # --- check if selected keyword really exist into the Main keyword service Table ---
        # ----------------------------------------------------------------------------------
        keywordObject  = KeywordService.objects.filter(keyword=keyword)
        if not keywordObject:
            keywordObject  = KeywordService.objects.filter(id=keyword_id)
            if keywordObject:
                keywordObj  = keywordObject[0]
        else:
            keywordObj  = keywordObject[0]
        # ----------------------------------------------------------------
        # --- try to check if this keyword still exist in User keyword ---
        # ----------------------------------------------------------------
        if not keywordObj:
            keywordObject  = UserKeywordService.objects.filter(keyword=keyword, is_accepted=True)
            if not keywordObject:
                keywordObject  = UserKeywordService.objects.filter(id=keyword_id, is_accepted=True)
                if keywordObject:
                    addExistingUserKeyword = True
                    keywordObj  = keywordObject[0]
            else:
                addExistingUserKeyword = True
                keywordObj  = keywordObject[0]

    # ---------------------------------------------------------
    # ---------------------------------------------------------
    # ---    U S E R        K E Y W O R D S                 ---
    # --- Store each new user keywords                      ---
    # ---------------------------------------------------------
    # ---------------------------------------------------------
    else:
        if userObj:
            listKeywords = parsString(keyword)
            for keyword in listKeywords:

                # -----------------------------------------------------------
                # -- (1) First check if this User keyword already exist   ---
                # -- Validated or Not (neverMind) !!!                     ---
                # -----------------------------------------------------------
                keywordObj = extractUserKeywords(userObj.user, keyword=keyword, allstatus=True, single=True)

                # -----------------------------------------------------------
                # -- 2) This user Keyword does not yet exist              ---
                # -- it should first of all created UserKeywordservice    ---
                # -----------------------------------------------------------
                if not keywordObj:
                    keywordObj = createUserKeyword(keyword, userObj.user)

                # ------------------------------------------------------------------------------
                # --- 3) check if this user keyword is already attached to User profile      ---
                # ------------------------------------------------------------------------------
                if keywordObj:
                    keywordObjUser  = UserProfile.objects.filter(user_keywords__keyword=keywordObj, user=userObj.user)
                    if keywordObjUser:
                        status ="error"
                        msg_error = "User Keyword already added"
                    else:
                        userObj.user_keywords.add(keywordObj)
                        userObj.save()

                        # ---------------------------------
                        # --- send Notifications        ---
                        adminUser = getAdminUser()
                        for eachAdmin in adminUser:
                            # --- Send Notification to admin Staff ---
                            message = 'New User Keywords have been created by (%s)' % currentUser.email
                            SendMessage(None, None, currentUser, eachAdmin, Message.USERKEYWORD, Message.MESSAGE_SUBJECT[Message.USERKEYWORD], message, extras=keywordObj)
                            # --- send email to web admin         ---
                            argument = {'count' : 1, 'user' : currentUser, 'keywords' : [keywordObj]}
                            send_email(eachAdmin.email, 'pending_userkeywords', argument, '')



    # --------------------------------------------------------------------------------------------
    # ---- Update the current User Profile record and save it (only if no duplicate or error) ----
    # ----   Only for Builtin Keywords                                                        ----
    # --------------------------------------------------------------------------------------------
    if status == 'ok' and not customerUserKeyword and not addExistingUserKeyword and keywordObj:
        userObj.keywords.add(keywordObj)
        userObj.save()
    elif addExistingUserKeyword and keywordObj:
        userObj.user_keywords.add(keywordObj)
        userObj.save()


    # -------------------------------------------------------------------
    # ---- Relist all Keywords attached to this user profile (max 6) ----
    # ---- Standard and/or User keywords (M2M) relationShip          ----
    # -------------------------------------------------------------------
    if keywordObj:
        userKeywordList = userObj.user_keywords.all()
        keywordList = userObj.keywords.all()
        nbrKeywords = len (keywordList)
        nbrUserKeywords = len(userKeywordList)

    # -------------------------------------------------------------------
    # ---- Finally prepare and render Json Object                    ----
    # -------------------------------------------------------------------
    ctx = {
        'user': userObj,
        'items' : keywordList,
        'items_user' : userKeywordList,
        'total_count' : nbrKeywords + nbrUserKeywords,
           }
    html = render_to_string(template_name, ctx, context_instance=RequestContext(request))
    return {
        "status": status,
        "msg_error": msg_error,
        "html": html,
        "total_count": nbrKeywords + nbrUserKeywords,
    }


@login_required
@json_view
def delete_keyword(request, user):
    """
    add a new Keyword to Userprofile
    UserprofileOb = UserProfile.objects.filter()   // get Userprofile record Object/Id
    KeywordsObj = KeywordService.objects.filter()  // get keyword record Object/Id
    UserprofileOb.keywords.add(KeywordsObj)        // add to M2M table the new keywords for the current User
    ====> We can several Keywords add the same time add(ccc, gggg)
    UserprofileOb.save()                           // finally save the Current Userprofile record
    --------------------------------------------------------------------
    For User's Keyword not yet approved please use same logic for UserkeywordService
    User keywords with origin(account) and Mode(user)
    """

    status = "ok"
    keywordObj = None
    template_name = 'account/block-keywords.html'
    keyword = request.POST.get('keyword')
    keyword_id = request.POST.get('id')
    currentUser = request.user


    # -------------------------------------------
    # --- Get User's Profile Record           ---
    # -------------------------------------------
    userProfileObject =   UserProfile.objects.filter(id=user)
    if userProfileObject:
        userObj = userProfileObject[0]

    # ----------------------------------------------------------
    # --- try to access to Keywords to be deleted (Standard) ---
    # ----------------------------------------------------------
    keywordObject  = KeywordService.objects.filter(keyword=keyword)
    if not keywordObject:
        keywordObject  = KeywordService.objects.filter(id=keyword_id)
        if keywordObject:
            keywordObj  = keywordObject[0]
    else:
        keywordObj  = keywordObject[0]

    # ------------------------------------------------------------
    # ---- Update the current User Profile record and save it ----
    # ---- remove Standard keyword or User Keyword            ----
    # ------------------------------------------------------------
    if keywordObj:
        userObj.keywords.remove(keywordObj)
        userObj.save()
    else:
        keywordObj = extractUserKeywords(currentUser, keyword=keyword_id, allstatus=True, single=True)
        if keywordObj:
            keywordObjUser  = UserProfile.objects.filter(user_keywords__id=keywordObj.id, user=userObj.user).exists()
            if keywordObjUser:
                userObj.user_keywords.remove(keywordObj)
                userObj.save()

    # -------------------------------------------------------------------
    # ---- Relist all Keywords attached to this user profile (max 6) ----
    # -------------------------------------------------------------------
    keywordList = userObj.keywords.all()
    userKeywordList = userObj.user_keywords.all()
    nbrKeywords = len (keywordList)
    nbrKeywordsuser = len (userKeywordList)


    ctx = {
        'user': userObj,
        'items' : keywordList,
        'items_user' : userKeywordList,
        'total_count' : nbrKeywords + nbrKeywordsuser,
           }
    html = render_to_string(template_name, ctx, context_instance=RequestContext(request))
    return {
        "status": status,
        "html": html,
        "total_count": nbrKeywords + nbrKeywordsuser,
    }





@login_required
@json_view
def user_list_keywords(request, user, mode=''):
    """
    Return list of keywords related to member/user.

    """


    template_name = 'account/block-keywords.html'
    currentUser = request.user

    # ------------------------------------------
    # --- extract User profile data          ---
    userProfileObject =   UserProfile.objects.filter(id=user)
    if userProfileObject:
        userObj = userProfileObject[0]

    # ----------------------------------------------------------------------
    # --- extract all Keywords (std and User)  for the selected member -----
    keywordList = userObj.keywords.all()
    userKeywordList = userObj.user_keywords.all()

    nbrKeywords = len (keywordList)
    nbrUserKeywords = len (userKeywordList)

    # ----------------------------------
    # ---- prepare Html rendering ------
    ctx = {
        'items': keywordList,
        'items_user': userKeywordList,
        'total_count': nbrKeywords + nbrUserKeywords,
    }

    # -------------------------------------------
    # --- Html rendering                      ---
    html = render_to_string(template_name, ctx, context_instance=RequestContext(request))
    return {
        "html": html,
        "total_count": nbrKeywords + nbrUserKeywords,
    }


@login_required
@json_view
def old_user_add_alert(request, user):
    """
    create anew Ad Alert for the current user

    -------------------------------------------------------------------------------------
    user = models.ForeignKey(UserProfile, related_name='alert_user')
    type = models.CharField(max_length=15, db_index=True, choices=ALERT_TYPE)
    distance = models.IntegerField(default=2)
    frequency = models.CharField(max_length=15, db_index=True, choices=ALERT_FREQUENCY)
    location_address = models.CharField(max_length=255, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    activated = models.BooleanField(default=True)
    status  = models.CharField(max_length=15, db_index=True, choices=ALERT_STATUS)
    keywords = models.ManyToManyField(KeywordService, related_name='alert_keywords')
    ----------------------------------------------------------------------------------------

    """

    status = "ok"
    template_name = 'account/block-current-ad-alerts.html'
    keyword = request.POST.get('keyword')
    keyword_id = request.POST.get('keyword_id')
    location = request.POST.get('location')
    distance = request.POST.get('distance')
    latitude = request.POST.get('latitude')
    longitude = request.POST.get('longitude')
    frequency = request.POST.get('frequency')
    nbrAlerts = 0

    # --------------------------------------
    # --- retrieve UserProfile Record    ---
    userProfileObject =   UserProfile.objects.filter(id=user)
    if userProfileObject:
        userObj = userProfileObject[0]

    # ------------------------------
    # ---- Get  Keywords Record ----
    keywordObject  = KeywordService.objects.filter(keyword=keyword)
    if not keywordObject:
        keywordObject  = KeywordService.objects.filter(id=keyword_id)
        if keywordObject:
            keywordObj  = keywordObject[0]
    else:
        keywordObj  = keywordObject[0]

    # ------------------------------------------------------------
    # ---- Create a New alert record                          ----
    alertObj = AlertAd.objects.create(user=userObj,
        location_address= location,
        distance=distance,
        latitude=latitude,
        longitude=longitude,
        frequency=frequency,
        activated=True,
        type = 'ad'
        )
    alertObj.keywords.add(keywordObj)
    alertObj.save()

    # --------------------------------------------------------------
    # ---- Relist all Existing AD Alerts  attached to this user ----
    alertList = AlertAd.objects.filter(user=user)
    nbrAlerts = len (alertList)


    ctx = {
        'user': userObj,
        'alerts' : alertList,
        'total_count' : nbrAlerts,
           }
    html = render_to_string(template_name, ctx, context_instance=RequestContext(request))
    return {
        "status": status,
        "html": html,
        "total_count": nbrAlerts,
    }


def get_user_currency(latitude, longitude, default=None):
    from xauto.googlemap.googlemaps import GoogleMaps
    try:
        gmaps = GoogleMaps(settings.DEVELOPER_KEY)
        reverse_value = gmaps.reverse_geocode(latitude, longitude)
        country_code = reverse_value['Placemark'][0]['AddressDetails']['Country']['CountryNameCode']
        return Currency.objects.get(country_code=country_code)
    except:
        return Currency.objects.get(country_code=settings.DEFAULT_COUNTRY)




@login_required
@json_view
def getAccountStat(request):
    """
    get the Job Buying stat (provider and customer)
    """

    status = "ok"
    msg_error = ""
    fromDate = '1900-01-01 00:00:00'
    currentUser = request.user
    currentProfile = UserProfile.objects.get(user=currentUser)
    returnModeLabel = ''

    dicStatConv = {
        'LAST_3_MONTHS' : 'LAST90',
        'LAST_6_MONTHS' : 'LAST180',
        'LAST_YEAR' : 'LASTYEAR',
        'ALL' : '',
        }
    dicStatConvlabel = {
        'LAST_3_MONTHS' : 'Last Three Months',
        'LAST_6_MONTHS' : 'Last Six Months',
        'LAST_YEAR' : 'Past Year',
        'ALL' : 'All Time',
        }

    # --------------------------------------
    # --- get range date                 ---
    mode   = request.POST.get('mode','')
    stat_mode   = request.POST.get('stat','buying')
    template_name = 'account/block-%s-activity.html' % stat_mode

    if mode:
        if mode in dicStatConv:
            keyDate = dicStatConv[mode]
            (fromDate, toDate) = getDateRangeStamp(keyDate)
            returnModeLabel = dicStatConvlabel[mode]


    # ------------------------------------------------------
    # --- compute Job stats for the current Logged user ----
    # ------------------------------------------------------

    if stat_mode == 'buying':
        countWorkingJobs = Job.objects.filter(author=currentUser, status=Job.STATUS_NEW, current_active_status=JobBid.STATUS_SELECTED, modified__gt=fromDate).count()
        countNotAwardedJobs = Job.objects.filter(author=currentUser, status=Job.STATUS_NEW, current_active_bid__isnull=True, modified__gt=fromDate).count()
        ctx = {
            'count_notwarded_events': countNotAwardedJobs,
            'count_working_events': countWorkingJobs,
            'user_id': currentUser.id,
        }
    else:
        countActiveJobs =  JobBid.objects.filter(provider=currentUser, status__in=JobBid.STATUS_OPEN_JOB, modified__gt=fromDate).count()
        countWorkedJobs = JobBid.objects.filter(provider=currentUser, status__in=JobBid.STATUS_VALID_JOB_STAT, modified__gt=fromDate).count()
        rating = FeedbackRating.active.all().filter(Q(author=currentUser) & Q(bid__status__in=JobBid.STATUS_COMPLETED_JOB) & Q(modified__gt=fromDate)).aggregate(average_rating=Avg('rating'))
        avgFeedback =  rating['average_rating'] if rating['average_rating'] else 0
        countFeedback = Feedback.objects.filter(Q(author=currentUser) & Q(bid__status__in=JobBid.STATUS_COMPLETED_JOB) & Q(modified__gt=fromDate)).count()

        ctx = {
            'count_active_events': countActiveJobs,
            'count_worked_events': countWorkedJobs,
            'average_feedback': avgFeedback,
            'count_feedback': countFeedback,
            'user_id': currentUser.id,
        }

    # ---------------------------------------------------------
    # ---- rendering output Html template for Job listing -----
    # ---------------------------------------------------------
    ctx['from'] = 'customer_profile'
    if 'HTTP_REFERER' in request.META and request.META['HTTP_REFERER'].endswith('/account/customer-profile/'):
        ctx['from'] = 'account'
    html = render_to_string(template_name, ctx, context_instance=RequestContext(request))
    return {
        "mode" : mode,
        "mode_label" : returnModeLabel,
        "status": status,
        "msg_error": msg_error,
        "html": html,
    }




def extractUserKeywords(currentUser, keyword=None, validated=False, rejected=False, single=False, allstatus=False, origin= 'account', mode='user', job=None, author=True):
    """
    Get all User's Keyword not yet validated (by default but could used to check validated one !!
    Work for Both user service Account and Job posted
    In Both case userkeyword will be attached to userprofile or Job thanks to a M2M relationship
    """

    possibleOrigin = ['account', 'job']
    if origin in possibleOrigin:
        selectorigin = possibleOrigin
    else:
        selectorigin = [origin]

    # ----------------------------------------------------------------------
    # --- Format the Query to access the User's keyword (account or Job) ---
    # ----------------------------------------------------------------------
    userKeywordList = []
    query = Q()
    if not allstatus:
        query = Q(is_rejected=rejected) & Q(is_accepted=validated) & Q(origin__in=selectorigin) & Q(mode = mode)
        query_keyword = Q(keyword=keyword) &  Q(author=currentUser)   &   Q(is_rejected=rejected) & Q(is_accepted=validated) & Q(origin__in=selectorigin) & Q(mode = mode)
        query_keyword_Pk = Q(pk=keyword)   &  Q(is_rejected=rejected) & Q(is_accepted=validated) & Q(origin__in=selectorigin) & Q(mode = mode)
        if job:
            query = query & Q(job=job)
        if author:
            query = query & Q(author=currentUser)
    else:
        query = Q(is_rejected=rejected) & Q(origin__in=selectorigin) & Q(mode = mode)
        query_keyword = Q(keyword=keyword)  &   Q(is_rejected=rejected) & Q(origin__in=selectorigin) & Q(mode = mode)
        query_keyword_Pk = Q(pk=keyword)    &   Q(is_rejected=rejected) & Q(origin__in=selectorigin) & Q(mode = mode)
        if job:
            query = query & Q(job=job)
        if author:
            query = query & Q(author=currentUser)

    # --------------------------------------------------------------------------------------
    # --- Extract User  Keywords by their accepted status (yes or Not)                   ---
    # --------------------------------------------------------------------------------------
    if not keyword:
        userKeywordList = UserKeywordService.objects.filter(query)
    else:
        try:
            userKeywordList = UserKeywordService.objects.filter(query_keyword)
            if not userKeywordList:
                if CheckNumeric(keyword):
                    userKeywordList = UserKeywordService.objects.filter(query_keyword_Pk)
        except:
            userKeywordList = UserKeywordService.objects.filter(query_keyword_Pk)


    # ----------------------------------------
    # -- Return  Tuples or Single record   ---
    # ----------------------------------------
    if single and userKeywordList:
        userKeywordList = userKeywordList[0]
    return userKeywordList

def createUserKeyword(keyword, user, job=None, mode='user', origin='account'):
    """
    common process to create a new user keyword
    """
    keywordObj = UserKeywordService.objects.create(
        keyword = keyword,
        author = user,
        date_added = datetime.datetime.now(),
        is_accepted = False,
        origin = origin,
        mode = mode,
        job=job
        )
    return keywordObj



@login_required
@json_view
def closeAccount(request):
    """
    closing account request
    """

    status = "ok"
    msg_error = ""
    redirect = ''
    currentUser = request.user

    # --------------------------------------
    # --- get Input parameters           ---
    # --------------------------------------
    mode   = request.POST.get('mode','')
    reason   = request.POST.get('reason','')

    # --------------------------------------
    # --- Update user acount (as Closed) ---
    # --------------------------------------
    if reason and currentUser:
        userProfileObject = UserProfile.objects.get(user=currentUser)
        if userProfileObject:

            # -------------------------------------
            # -- disable User profile           ---
            userProfileObject.is_closed = True
            userProfileObject.date_closed = datetime.datetime.now()
            userProfileObject.reason_closed = reason
            userProfileObject.save()
            msg_error = 'Your account(%s) has been closed - reason (%s)' % (currentUser.email, reason)

            # --------------------------------------------------
            # ---- Make inactive this user (on Django side) ----
            userObject = User.objects.get(pk=currentUser.id)
            if userObject:
                userObject.is_active = False
                userObject.save()

                # -- Logout and end Session ---
                logout(request)
                request.session.set_expiry(0)   # close session of Current Logger user

            adminUser = getAdminUser()

            # -----------------------------------------------
            # --- Send Email to Closed user and Web admin ---
            # -----------------------------------------------
            for eachTargetAdmin in adminUser:
                message = '(Admin) User[%s] Closed his account - Reason (%s)' % (currentUser.email, reason)
                SendMessage(None, None, currentUser, eachTargetAdmin, Message.CLOSEDA, Message.MESSAGE_SUBJECT[Message.CLOSEDA], message)
                # -----------------------------------------------
                # --- send email to admin user                ---
                argument = {'user' : currentUser, 'reason' : reason, 'mode' : 'admin',}
                send_email(eachTargetAdmin.email, 'close_account', argument, 'admin')

    ctx = {
        'close_reason' : reason,
        'user_id': currentUser.id,
        }

    # ---------------------------------------------------------
    # ---- rendering output Html template for Job listing -----
    # ---------------------------------------------------------
    return {
        "mode" : mode,
        "status": status,
        "msg_error": msg_error,
        "redirect" : redirect,
    }



user_images_view = login_required(UserProfileImagesView.as_view())
account_view = login_required(AccountView.as_view())
customer_profile_view = login_required(CustomerProfileView.as_view())
customer_profile_edit_view = login_required(CustomerProfileEditView.as_view())
service_profile_view = login_required(ServiceProfileView.as_view())
ad_alerts_view = login_required(AdAlertsView.as_view())
system_alerts_view = login_required(SystemAlertsView.as_view())

__all__ = ('account_view', 'customer_profile_view', 'service_profile_view', 'ad_alerts_view', 'system_alerts_view')