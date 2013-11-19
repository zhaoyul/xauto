from django.db import models
from django.contrib.auth.models import User, _
from django.conf import settings
from django.db.models import Avg, Count, Q, Sum
from xauto_lib.models import TimestampedModel
from xauto_lib.managers import manager_from
import sys

from datetime import timedelta, datetime
import sys, string


class EventKeywordManager(object):
    """
    Custom manager mixin for event keywords, selecting active keywords .
    """
    def active(self):
        return self.filter(is_active=True)

    def with_active(self):
        results = []
        from event.models import Event
        allRecords = self.all()
        for keyword in allRecords:
            keyword.num_events = Event.active.filter(
                keywords__keyword__startswith=keyword.keyword).count()
            if keyword.num_events > 0:
                results.append(keyword)
        return results

    def with_active_count(self):
        ctrCountEvent = 0
        from event.models import Event
        allRecords = self.all()
        for keyword in allRecords:
            keyword.num_events = Event.active.filter(
                keywords__keyword__startswith=keyword.keyword).count()
            if keyword.num_events > 0:
                ctrCountEvent += keyword.num_events
        return ctrCountEvent


class Category(TimestampedModel):

    name = models.CharField(max_length=255)
    parent = models.ForeignKey('keywords.MainKeywordService', null=True, blank=True, related_name='parent_category')
    can_add = models.BooleanField(default=False)
    owner = models.ForeignKey(User, null=True, blank=True, related_name='category_owner')
    date_add = models.DateTimeField(auto_now_add=True)
    objects = manager_from(EventKeywordManager)

    class Meta:
        verbose_name_plural = 'Categories'
        unique_together = [('parent', 'name')]
        ordering = ['can_add', 'name']

    def __unicode__(self):
        return u'%s' % self.name


class MainKeywordService(TimestampedModel):
    """
    Main xauto Keyword Parent Database for the search engine (releated name to Event Table).
    """
    name = models.CharField(max_length=100, default='', db_index=True)
    description = models.TextField(blank=True, help_text="Meta description")
    is_active = models.BooleanField("active?", default=True)
    is_system = models.BooleanField("system?", default=False)
    icon = models.CharField(max_length=100, default='user')   # --- icon affected for each parent category/keyword ---
    event_count = models.PositiveIntegerField(default=0)                           # -- active Event for this keyword

    def __unicode__(self):
        return u"%s" % (self.name)



class SubCategKeywords(TimestampedModel):
    """
    Main xauto Keyword Sub Category Reference Database
    """
    name = models.CharField(max_length=100, default='', db_index=True)
    parent = models.ForeignKey(MainKeywordService, blank=False, null=True, related_name='main_subcateg_keyword')
    description = models.TextField(blank=True, help_text="Meta description")
    is_active = models.BooleanField("active?", default=True)
    is_system = models.BooleanField("system?", default=False)
    is_hidden = models.BooleanField("Hide?", default=False)                    # --- Hidde this sub category ---
    event_count = models.PositiveIntegerField(default=0)                           # -- active Event for this keyword
    migrated = models.BooleanField("Migrated ?", default=False)                  # --- account Page and Post Event Page

    def __unicode__(self):
        return u"%s" % (self.name)




class KeywordService(TimestampedModel):
    """
    xauto Keyword Database for the search engine (releated name to Event Table).
    """
    parent = models.ForeignKey(MainKeywordService, blank=True, null=True, related_name='main_keyword')
    keyword = models.CharField(max_length=100, default='')
    sub_category = models.ForeignKey(SubCategKeywords, blank=True, null=True, related_name='sub_category')        #
    link_keyword = models.CharField(max_length=100, default='', db_index=True, null=True, blank=True)     #
    link_keyword2 = models.CharField(max_length=100, default='', db_index=True, null=True, blank=True)    #
    link_keyword3 = models.CharField(max_length=100, default='', db_index=True, null=True, blank=True)    #
    description = models.TextField(blank=True, help_text="Meta description")
    is_active = models.BooleanField("active?", default=True)                     # --- activate pr deactivate a keyword
    is_system = models.BooleanField("system?", default=False)                    # --- System admin only  /backend admin
    is_event = models.BooleanField("Event Page?", default=False)             # --- Find Work > Category Page
    can_add = models.BooleanField("Can add?", default=True)                      # --- account Page and Post Event Page
    event_count = models.PositiveIntegerField(default=0)                           # -- active Event for this keyword
    owner = models.ForeignKey(User, null=True, blank=True)
    date_add = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    migrated = models.BooleanField("Migrated ?", default=False)                  # --- account Page and Post Event Page
    position = models.PositiveSmallIntegerField("Position")


    def __unicode__(self):
        if self.parent is not None:
            return u"%s-%s" % (self.keyword,  self.parent)
        else:
            return self.keyword

    def save(self, **kwargs):
        super(KeywordService, self).save(**kwargs)

    def active_events(self):
        """
        Return queryset selecting active Events for this keyword.
        """
        from event.models import Event

        qs = Event.valids.active().filter(keyword__startswith=self.keyword)

        return qs

    @staticmethod
    def autocomplete_search_fields():
            return ("id__iexact", "keyword__icontains",)

class UserKeywordService(TimestampedModel):
    """
    xauto User Keyword Database (temporary storage)
    """

    WORK_ORIGIN = 'event'
    PROVIDER_ORIGIN = 'service'

    ORIGIN_CHOICES = (
        ('event', 'Event'),
        ('account', 'Account'),
        ('service', 'Find Services'),
        ('work', 'Find Work'),
    )

    MODE_CHOICES = (
        ('user', 'User'),
        ('popular', 'Popular'),
    )

    parent = models.ForeignKey(MainKeywordService, blank=True, null=True, related_name='user_keyword')
    keyword = models.CharField(max_length=100, default='', db_index=True)
    sub_category = models.ForeignKey(SubCategKeywords, blank=True, null=True, related_name='user_sub_category')        #
    author = models.ForeignKey(User, related_name='author_keywords', blank=True, null=True)
    is_rejected = models.BooleanField("rejected?", default=False)
    is_accepted = models.BooleanField("validated?", default=False)
    reason  = models.CharField(max_length=100, default='', db_index=True)
    date_migrated = models.DateTimeField(blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    event = models.ForeignKey('event.Event', related_name='author_keywords_event', blank=True, null=True)
    nbr_same = models.IntegerField(default=1)
    origin = models.CharField(max_length=50, choices=ORIGIN_CHOICES, default='event')
    mode = models.CharField(max_length=50, choices=MODE_CHOICES, default='user')
    email_sent = models.BooleanField("Email sent?", default=False)
    event_posted = models.BooleanField("Event Posted ?", default=False)

    def __unicode__(self):
        if self.parent is not None:
            return u"%s-%s" % (self.keyword,  self.parent)
        else:
            return self.keyword

    def save(self, **kwargs):
        super(UserKeywordService, self).save(**kwargs)


    def eventName(self):
        if self.event:
            return '<a title="Click to Edit the Event record" href ="/admin/core/event/%s/"><strong><span style="color: #309BBF;">%s</span></strong></a>' % (self.event.id, self.event.headline)
        else:
            return ''


    eventName.allow_tags = True



class ForbiddenUserKeywordService(TimestampedModel):
    """
    xauto User Keyword Forbidden Database
    """
    keyword = models.CharField(max_length=100, default='', db_index=True)
    is_forbidden = models.BooleanField("Forbidden?", default=True)
    reason  = models.CharField(max_length=100, default='', db_index=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        if self.parent is not None:
            return u"%s-%s" % (self.keyword,  self.reason)
        else:
            return self.keyword

    def save(self, **kwargs):
        super(ForbiddenUserKeywordService, self).save(**kwargs)


def UpdateUserKeyword(currentUser, origin='event', mode='user', keydata=''):
    # --------------------------------------------------
    # --- store most popular search keywords         ---
    # --------------------------------------------------
    arrayKeyword = []
    objKeyword =  None
    reformattedKeyword = string.split(keydata, ' ')
    for eachKey in reformattedKeyword:
        if eachKey:
            arrayKeyword.append(eachKey.strip())
    keydata = string.join(arrayKeyword, ' ')

    userAuthor = None
    if not currentUser.is_anonymous:
        userAuthor = currentUser

    userkeyword = UserKeywordService.objects.filter(mode=mode, origin=origin, keyword=keydata)
    if not userkeyword:
        objKeyword = UserKeywordService.objects.create(
            keyword = keydata,
            author = userAuthor,
            date_added = datetime.now(),
            origin = origin,
            mode = mode,
            nbr_same = 1
            )
    else:
        objKeyword = userkeyword[0]
        nbrSame = objKeyword.nbr_same
        nbrSame += 1
        objKeyword.nbr_same = nbrSame
        objKeyword.save()

    return objKeyword


# ------------------------------------------------------------
# -- old keywords database
# ------------------------------------------------------------

class KeywordService2(TimestampedModel):
    """
    Servicei Keyword Database for the search engine (releated name to Job Table).
    """
    parent = models.ForeignKey('MainKeywordService2', blank=True, null=True, related_name='main_keyword2')
    keyword = models.CharField(max_length=100, default='')
    category = models.ForeignKey(Category, blank=True, null=True, related_name='main_category2')           #
    sub_category = models.ForeignKey('SubCategKeywords2', blank=True, null=True, related_name='sub_category2')        #
    link_keyword = models.CharField(max_length=100, default='', db_index=True, null=True, blank=True)     #
    link_keyword2 = models.CharField(max_length=100, default='', db_index=True, null=True, blank=True)    #
    link_keyword3 = models.CharField(max_length=100, default='', db_index=True, null=True, blank=True)    #
    description = models.TextField(blank=True, help_text="Meta description")
    is_active = models.BooleanField("active?", default=True)                     # --- activate pr deactivate a keyword
    is_system = models.BooleanField("system?", default=False)                    # --- System admin only  /backend admin
    is_job_catpage = models.BooleanField("Job Page?", default=False)             # --- Find Work > Category Page
    is_provider_catpage = models.BooleanField("Provider Page?", default=False)   # --- Find provider > Category Page
    is_header_search = models.BooleanField("Header Search?", default=True)       # --- Header Search Page
    is_account_page = models.BooleanField("Account Page?", default=True)
    can_add = models.BooleanField("Can add?", default=True)                      # --- account Page and Post Job Page
    job_count = models.PositiveIntegerField(default=0)                           # -- active Job for this keyword
    provider_count = models.PositiveIntegerField(default=0)                      # -- active providers for this keyword
    owner = models.ForeignKey(User, null=True, blank=True)
    date_add = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    migrated = models.BooleanField("Migrated ?", default=False)                  # --- account Page and Post Job Page
    position = models.PositiveSmallIntegerField("Position")


    def __unicode__(self):
        if self.parent is not None:
            return u"%s-%s" % (self.keyword,  self.parent)
        else:
            return self.keyword

    def save(self, **kwargs):
        super(KeywordService, self).save(**kwargs)

    def active_jobs(self):
        """
        Return queryset selecting active Jobs for this keyword.
        """
        from core.models import Job

        qs = Job.valids.active().filter(keyword__startswith=self.keyword)

        return qs

    @staticmethod
    def autocomplete_search_fields():
            return ("id__iexact", "keyword__icontains",)



class SubCategKeywords2(TimestampedModel):
    """
    Main Servicei Keyword Sub Category Reference Database
    """
    name = models.CharField(max_length=100, default='', db_index=True)
    parent = models.ForeignKey('MainKeywordService2', blank=False, null=True, related_name='main_subcateg_keyword2')
    description = models.TextField(blank=True, help_text="Meta description")
    is_active = models.BooleanField("active?", default=True)
    is_system = models.BooleanField("system?", default=False)
    is_hidden = models.BooleanField("Hide?", default=False)                    # --- Hidde this sub category ---
    job_count = models.PositiveIntegerField(default=0)                           # -- active Job for this keyword
    provider_count = models.PositiveIntegerField(default=0)                      # -- active providers for this keyword
    migrated = models.BooleanField("Migrated ?", default=False)                  # --- account Page and Post Job Page

    def __unicode__(self):
        return u"%s" % (self.name)



class MainKeywordService2(TimestampedModel):
    """
    Main Servicei Keyword Parent Database for the search engine (releated name to Job Table).
    """
    name = models.CharField(max_length=100, default='', db_index=True)
    description = models.TextField(blank=True, help_text="Meta description")
    is_active = models.BooleanField("active?", default=True)
    is_system = models.BooleanField("system?", default=False)
    icon = models.CharField(max_length=100, default='user')   # --- icon affected for each parent category/keyword ---
    job_count = models.PositiveIntegerField(default=0)                           # -- active Job for this keyword
    provider_count = models.PositiveIntegerField(default=0)                      # -- active providers for this keyword


    def __unicode__(self):
        return u"%s" % (self.name)








