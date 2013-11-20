from django.db import models
from django.contrib.auth.models import _

from xauto_lib.models import TimestampedModel
from keywords.models import KeywordService, UserKeywordService
from member.models import UserProfile


class AlertEvent(TimestampedModel):


    EVENT_ALERT = 'event'
    SYSTEM_ALERT = 'system'

    ALERT_TYPE = (
        (EVENT_ALERT, 'Event Alerts'),
        (SYSTEM_ALERT, 'System Alerts') )

    ALERT_FREQUENCY = (
        ('immediatly', 'Immediately'),
        ('day', 'Daily Digest'),
        ('week', 'Weekly Digest'),
    )

    ALERT_STATUS = (
        ('pending', 'Pending Alert'),
        ('executed', 'Executed Alert') )

    user = models.ForeignKey(UserProfile, related_name='alert_user')
    event = models.ForeignKey('event.Event', related_name='alert_user_event', null=True, blank=True)
    type = models.CharField(max_length=15, db_index=True, choices=ALERT_TYPE)
    distance = models.IntegerField(default=2)
    frequency = models.CharField(max_length=15, db_index=True, choices=ALERT_FREQUENCY)
    location_address = models.CharField(max_length=255, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    activated = models.BooleanField(default=True)
    status  = models.CharField(max_length=15, db_index=True, choices=ALERT_STATUS)
    keywords = models.ManyToManyField(KeywordService, related_name='alert_keywords')
    user_keywords = models.ManyToManyField(UserKeywordService, related_name='alert_user_keywords')
    sent = models.BooleanField(default=False)
    last_sent_at = models.DateTimeField(null=True)
    received_at = models.DateTimeField(null=True)
    nbr_alert = models.IntegerField(default=0)
    nbr_sent = models.IntegerField(default=0)
    is_send_email = models.BooleanField(default=True)

    def __unicode__(self):
        return '%s-%s-%s' % (self.user.user.username, self.type, self.frequency)


class AlertSystem(TimestampedModel):

    ALERT_FREQUENCY = (
        ('immediate', 'Immediately'),
        ('day', 'Daily Digest'),
        ('week', 'Weekly Digest'),
    )

    user = models.ForeignKey(UserProfile, related_name='alert_system_user')
    signup  = models.BooleanField(default=True, verbose_name='User Signup')
    activation  = models.BooleanField(default=True, verbose_name='Account Activation')
    password_recovery  = models.BooleanField(default=True, verbose_name='Password recovery')
    new_message_received  = models.BooleanField(default=False, verbose_name='New message Received')
    feedback_received  = models.BooleanField(default=False, verbose_name='Feeback received')

    attendee_registred = models.BooleanField(default=False, verbose_name='Event register received')
    frequency_attendee = models.CharField(max_length=15, db_index=True, choices=ALERT_FREQUENCY, verbose_name='New message Alert Frequency' ,default='immediate')

    nbr_email = models.IntegerField(default=0)
    nbr_alert = models.IntegerField(default=0)
    last_sent_email = models.DateTimeField(null=True)

    def __unicode__(self):
        return '%s' % (self.user.user.last_name)



class AlertSent(TimestampedModel):
    """
    Table to store which notification for each Event has been sent for given user
    """

    SYSTEM_ALERT = 'system'
    EVENT_ALERT = 'event'

    ALERT_FREQUENCY = (
        ('immediatly', 'Immediately'),
        ('day', 'Daily Digest'),
        ('week', 'Weekly Digest'),
    )

    ALERT_TYPE = (
        (EVENT_ALERT, 'Event Alerts'),
        (SYSTEM_ALERT, 'System Alerts') )

    user = models.ForeignKey(UserProfile, related_name='alert_sent_user')
    alert = models.ForeignKey(AlertEvent, blank=True, null=True, related_name='alertad_sent_user')
    alert_system = models.ForeignKey(AlertSystem, blank=True, null=True, related_name='alertsys_sent_user')
    sent_at = models.DateTimeField(null=True)
    event = models.ForeignKey('event.Event', related_name='alert_authored_events')
    message = models.ForeignKey('member.Message', blank=True, null=True, related_name='alert_authored_message')
    frequency = models.CharField(max_length=15, db_index=True, choices=ALERT_FREQUENCY)
    type_alert = models.CharField(choices=ALERT_TYPE, max_length=10, default=EVENT_ALERT)

    def __unicode__(self):
        if self.event:
            return '%s-%s-%s-%s-%s' % (self.user.user.username, self.frequency, self.event.title, self.alert.id, self.type_alert)
        else:
            return '%s-%s-%s-%s' % (self.user.username, self.frequency, self.alert.id, self.type_alert)


class Application(TimestampedModel):
    application = models.CharField(max_length=50, verbose_name=_('Django Application'))
    description = models.CharField(max_length=255, blank=False, null=False)

    def __unicode__(self):
        return '%s' % (self.application)


class Parameters(TimestampedModel):
    """
    Golbal xauto Mysql Models for various dynamic and static Parameters
    """

    STATIC_APPLICATION = 'STATIC'
    FLAT_APPLICATION = 'FLAT'
    TOS_APPLICATION = 'TOS'
    PRIVACY_APPLICATION = 'PRIVACY'
    EVENT_APPLICATION = 'EVENT'

    # ---------------------------------
    # --- Privacy Keywords          ---
    POLICY = 'POLICY'
    PRIVACY_YOUR = 'PRIVACY_YOUR'

    # -------------------------------
    # ---- define Group  keywords ---
    CONTACT_SELECTION = 'contact'
    ABOUT = 'about'
    HELP = 'help'
    FOOTER = 'footer'
    TOS = 'terms'
    PRIVACY = 'privacy'
    EVENTDETAILS = 'eventdetails'
    REPORT = 'report'

    # ------------------------------
    # ---- define Key   keywords ---
    DEPARTMENT = 'DEPARTMENT'
    CANCEL_REASON = 'cancel_reason'
    ABOUT_SERVICE = 'about_xauto'
    CEO = 'ceo'
    DEVElOPPER = 'developper'
    WHAT_MEMBER_CUSTOMER = 'what_customer'
    WHAT_MEMBER_PROVIDER = 'what_provider'
    ABOUT_TEXT = 'about_text'
    ABOUT_CEO = 'CEO'
    ABOUT_DEV_1 = 'DEV1'
    HELP_CONTENT = 'help'
    HELP_URL = 'help_url'
    FOOTER_ADVERTISE = 'advertise'
    COPYRIGHT = 'copyright'
    CANCEL = 'CANCEL'
    FLAGEVENT = 'FLAGEVENT'
    REPORT = 'report'
    CLOSE_ACCOUNT = 'close_account'

    # ---------------------------------------
    # -- Terms of Services Keywords       ---
    TOS_SERVICE = 'termsofservice'
    TOS_DEFINTION = 'tos_definition'
    TOS_OVERVIEW = 'tos_overview'
    TOS_REGISTRATION =  'tos_registration'
    TOS_RELATION = 'tos_relation'
    TOS_RESTRICTION = 'tos_restriction'
    TOS_TERMINATION = 'tos_termination'
    TOS_FEES = 'tos_fees'
    TOS_PROPERTY = 'tos_property'
    TOS_DISCLAIMER = 'tos_disclaimer'
    TOS_CONDITIONS = 'tos_conditions'

    # -------------------------------------
    # -- Terms of uses definition  group --

    TOS_GROUP = [
        TOS_SERVICE,
        TOS_DEFINTION,
        TOS_OVERVIEW ,
        TOS_REGISTRATION ,
        TOS_RELATION ,
        TOS_RESTRICTION ,
        TOS_TERMINATION ,
        TOS_FEES ,
        TOS_PROPERTY ,
        TOS_DISCLAIMER ,
        TOS_CONDITIONS ,

        ]

    PRIVACY_GROUP = [
        POLICY ,
        PRIVACY_YOUR,
        ]


    GROUP_PARAMETER = (
        (CONTACT_SELECTION, 'Contact Page'),
        (ABOUT, 'About Page'),
        (HELP, 'Help Page'),
        (FOOTER, 'Footer Content'),
        (TOS, 'Terms of use'),
        (PRIVACY, 'Privacy Policy'),
        (CANCEL, 'Cancel Event'),
        (REPORT, 'Report Event'),
    )

    KEY_PARAMETER = (
        (CLOSE_ACCOUNT, 'Close an Account'),
        (EVENT_APPLICATION, 'Flag an Event'),
        (ABOUT_SERVICE, 'About xauto'),
        (ABOUT_TEXT, 'About Explanation (Customer and Provider)'),
        (ABOUT_CEO, 'About CEO of xauto'),
        (ABOUT_DEV_1, 'About xauto developper'),
        (CEO, 'Ceo information'),
        (DEVElOPPER, 'Developper information'),
        (HELP_CONTENT, 'Help Content (Data and Url)'),
        (FOOTER_ADVERTISE, 'Footer Adverstise Content'),
        (COPYRIGHT, 'xauto CopyRight'),
        (POLICY, 'Privacy Policy'),
        (PRIVACY_YOUR, PRIVACY_YOUR),
    )

    application = models.ForeignKey(Application, verbose_name=_('Django Application'))
    group = models.CharField(choices=GROUP_PARAMETER, max_length=100, blank=False, null=False, default=CONTACT_SELECTION)
    key = models.CharField(choices=KEY_PARAMETER, max_length=100, blank=False, null=False, default=DEPARTMENT)
    label = models.CharField(max_length=100, blank=True, null=True)
    value = models.CharField(max_length=1024, blank=True)
    title = models.CharField(max_length=255, blank=True)
    sequence = models.IntegerField(default=1)
    flatpage = models.BooleanField(default=False)
    staticpage = models.BooleanField(default=False)
    enable = models.BooleanField(default=True)
    help = models.BooleanField(default=False)
    array = models.BooleanField(default=False)
    description = models.TextField(default='', blank=True, null=True)
    url_href = models.TextField(default='', blank=True, null=True, verbose_name='Url and Href Link')

    def __unicode__(self):
        return '%s-%s-%s-%s' % (self.application, self.group, self.key, self.value)


