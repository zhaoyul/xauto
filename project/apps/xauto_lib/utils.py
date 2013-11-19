from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.sites.models import Site
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from xauto_lib.calutil import getDateRangeStamp
from django.contrib.auth.models import User

from livesettings import config_value
from xauto_lib import log

import re
import string, sys
import datetime
import ast
from urlparse import urljoin
from BeautifulSoup import BeautifulSoup, Comment
from xauto_utils.email import render_subject_message
from xauto_utils.email import django_send_mail


def send_email(email, template, argument, mode=''):

    # --------------------------------------------
    # ---- format base of Email               ----
    # --------------------------------------------
    templateEmail = 'EmailTemplates/%s.html' % template
    subject = 'EmailTemplates/%s_subject.html' % template

    subject, message = render_subject_message(
        subject,
        templateEmail,
        argument
        )

    emailTo = []
    emailToString = email
    emailTo.append(emailToString)
    log.tofile('send_mail', 'email [%s] sent to %s' % (subject, emailTo))
    django_send_mail(subject, message, emailTo, from_email=settings.DEFAULT_FROM_EMAIL)

    # --------------------------------------------
    # ---- Send email to xauto admin staff ----
    # --------------------------------------------
    if mode == 'admin':
        if mode in settings.ADMIN_EMAIL_CONTACT:
            listAdminEmail = settings.ADMIN_EMAIL_CONTACT[mode]
            for eachAdminEmail in  listAdminEmail:
                emailTo = []
                emailTo.append(eachAdminEmail)
                django_send_mail(subject, message, emailTo, from_email=settings.DEFAULT_FROM_EMAIL)



def checkDuplicateList(selList):
    """
    check duplicate in Array or Dic
    """
    tmp = []
    for row in selList:
        if tmp.__contains__(row):
            return row
        else:
            tmp.append(row)
    return False


def parsString(stringValue, delimiter=',', output='array', duplicate=False):
    """
    parse string and convert it to list or array
    """

    ctrValue = 0
    if output == 'array':
        arrayValue = []
    else:
        arrayValue = {}

    reader = string.split(stringValue, delimiter)
    for row in reader:
        if output == 'array':
            if (not arrayValue.__contains__(row) and not duplicate) or duplicate:
                ctrValue += 1
                arrayValue.append(string.strip(row))
        else:
            if row not in arrayValue:
                ctrValue += 1
                arrayValue[string.strip(row)] = '*'

    return arrayValue



class Choices(dict):
    """
    A dictionary which behaves like a tuple/list thingie for django choice lists.
    """
    def __new__(cls, *args):
        obj = super(Choices, cls).__new__(cls)
        if args:
            obj._orig = list(args[0])
            obj.update(enumerate(*args))
        return obj

    def __len__(self):
        return len(self._orig)

    def __iter__(self):
        return iter(self._orig)

    @property
    def default(self):
        """default choice is the first key"""
        return self[0][0]

    def find(self, value, default=None):
        "Find the key for a verbose value (inverse lookup)"
        ind = [y for x,y in self].index(value)
        if ind == -1: return default
        return self._orig[ind][0]

    def index(self, value):
        "Given a key, value, or (key, value) tuple, find the index"
        ind = [x for x,y in self].index(value)
        if ind == -1:
            ind = [y for x,y in self].index(value)
        if ind == -1:
            ind = self._orig.index(value)

        return ind

def mysql_get(modelsEntry, sqlKey, sqlValue, uniqValue = True, nbrOutput = 0):
    """
    First step of Mysql Error Handler (other Mysql Queries will added)
    """
    import ast
    try:
        kwargs = {sqlKey : sqlValue}
        if not uniqValue:
            ObjReturn = modelsEntry.objects.filter(**kwargs)
            if nbrOutput:
                if nbrOutput > 0 and ObjReturn:
                    ObjReturn = ObjReturn[nbrOutput - 1]
        else:
            ObjReturn = modelsEntry.objects.get(**kwargs)
        return ObjReturn
    except modelsEntry.DoesNotExist, err:
        return None


def flatten_errors(errors, prefix=""):
    if prefix: prefix += "-"
    return dict([(prefix + key, ", ".join(value)) for key, value in errors.items()])

def sanitizeHtml(value, base_url=None):
    """
    Safely clean input value, leaving only approved html tags.

    http://birdhouse.org/blog/2010/05/12/secure-user-input-with-django/
    """
    rjs = r'[\s]*(&#x.{1,7})?'.join(list('javascript:'))
    rvb = r'[\s]*(&#x.{1,7})?'.join(list('vbscript:'))
    re_scripts = re.compile('(%s)|(%s)' % (rjs, rvb), re.IGNORECASE)
    validTags = config_value('SITE', 'ALLOWED_HTML_TAGS').split()
    validAttrs = 'href src width height'.split()
    urlAttrs = 'href src'.split() # Attributes which should have a URL
    soup = BeautifulSoup(value)
    for comment in soup.findAll(text=lambda text: isinstance(text, Comment)):
        # Get rid of comments
        comment.extract()
    for tag in soup.findAll(True):
        if tag.name not in validTags:
            tag.hidden = True
        attrs = tag.attrs
        tag.attrs = []
        for attr, val in attrs:
            if attr in validAttrs:
                val = re_scripts.sub('', val) # Remove scripts (vbs & js)
                if attr in urlAttrs:
                    val = urljoin(base_url, val) # Calculate the absolute url
                tag.attrs.append((attr, val))
    return soup.renderContents().decode('utf8')

def safe_cmp(x, y, reverse=False):
    """
    A compare function for sorting an array in which some elements may be 'None',
    and the rest may be of a type which can't be compared to None.

    Usage::

        array.sort(lambda x, y: safe_cmp(x, y, [reverse]))
    """
    if x and y:
        result = cmp(x, y)
    elif x:
        result = 1
    elif y:
        result = -1
    else:
        result = 0

    return reverse and -result or result

def safe_max(*items):
    """
    A 'max' function which can handle 'None' values, when compared items are
    of a type which can't be compared to None.

    Usage::

        > safe_max([old date], None, [new date])
        new date
    """
    max_val = None
    for item in items:
        if max_val is None:
            max_val = item
        elif item is not None:
            max_val = max(max_val, item)
    return max_val

def send_mail(template, recipient_list, priority='medium',
              from_email=None, fail_silently=False, subject=None, mailer=True,
              **kwargs):
    """
    Send text and html email using mailer, falling back to text-only
    django sending if mailer isn't used.
    """
    if not from_email:
        from_email = settings.DEFAULT_FROM_EMAIL

    site = Site.objects.get_current()
    staticfiles_url = settings.STATIC_URL
    if staticfiles_url[:4] != 'http':
        staticfiles_url = 'http://%s%s' % (site.domain, staticfiles_url)

    ctx_dict = {
        'STATIC_URL': staticfiles_url,
        'site': site,
        'site_url': 'http://%s' % site.domain,
    }
    ctx_dict.update(kwargs)

    if subject is None:
        subject = render_to_string('email/%s.subject.txt' % template,
                                   ctx_dict).strip()

    message_plaintext = strip_tags(render_to_string('email/%s.txt' % template, ctx_dict))
    message_html = render_to_string('email/%s.html' % template, ctx_dict)

    #send_html_mail/send_mail needs to be imported here for testing emails.
    if settings.EMAIL_BACKEND[:13 ] == "django_mailer" and mailer==True:
        #from django_mailer_html import send_mail_html as send_mail
        from django_mailer import send_mail as send_mail
        use_mailer = True
    else:
        from django.core.mail import mail_managers as django_send_mail
        use_mailer = False

    if use_mailer:
        send_mail(subject, message_html, from_email, recipient_list)
        #mail_admins(subject, message_html)
        return True
    else:
        return commonHtmlEmail(subject, message_plaintext, message_html, from_email, recipient_list,  fail_silently=fail_silently)

def commonHtmlEmail(subject, messageText, messageHtml, fromEmail, toEmail, fail_silently=True):
    if fail_silently:
        try:
            toEmail = toEmail
            msg = EmailMultiAlternatives(subject, messageText, fromEmail, toEmail)
            msg.attach_alternative(messageHtml, "text/html")
            msg.send()
            return True
        except:
            return False
    else:
        # django.core.mail.backends.smtp
        toEmail = toEmail
        msg = EmailMultiAlternatives(subject, messageText, fromEmail, toEmail)
        msg.attach_alternative(messageHtml, "text/html")
        nbrSent = msg.send()
        return True

class ClassView():
    """
    this acts as a 'buffer' to make class based views thread safe

    usage:
    urlpatterns = patterns('accounts',
        url(r'^new/$', ClassView(views.NewBuild), name="new"),
    )

    http://djangosnippets.org/snippets/2049/
    """
    def __init__(self, class_name):
        """
        store the class name in an instance variable
        """
        self.class_name = class_name

    def __call__(self, request, *args, **kwargs):
        """
        Each time the class_view is invoked - for each request
        new-up a class_name and call it
        """
        view = self.class_name()
        return view(request, *args, **kwargs)


def FillCharacters(wzone, lenzone, valueChar = '', Direction='L'):

    ListBlank = RepeatCharacters(valueChar, lenzone)

    if wzone:
        wzone= string.strip(wzone)
        if wzone != '' and  lenzone > len(wzone):
            #============================================
            #==== padding with Blank on right side ======
            if Direction == 'L' :
                CtrFill = lenzone - len(wzone)
                if CtrFill > 0:
                    FillBlank = ListBlank[0:CtrFill]
                    wzone = wzone + FillBlank
            #============================================
            #==== padding with Blank on left  side ======
            else:
                wformat = '%(#)'+ str(lenzone) + 's'
                wzone = wformat  % {"#" : wzone}

    return wzone

def RepeatCharacters(Wcar,len=0):
    " == return a string with the Character repeteated Nnn times =="
    wzone = ''

    if Wcar and len > 0:
        for i in range(1,len+1):
            wzone += Wcar
    return wzone


def buildIDList(objRecord, keyName = 'id', mode = 'dic'):
    " for a given Record object, build a Mysql IN() List with Record ID() "
    if objRecord:
        if mode == 'dic':
            idString = string.join(map(str,objRecord.values(keyName)),',')
        else:
            idString = string.join(map(str,objRecord.values_list(keyName, flat=True)),',')
        return idString
    else:
        return None

def processError():
    exc_info = sys.exc_info()
    import traceback
    message = 'Traceback:\n%s\n\nRequest:\n' % ('\n'.join(traceback.format_exception(*exc_info)))
    log.tofile('buyer_payment_info', 'error [%s]' % (message), mode='local')
    return

def convertUnit(distance, direction='mi-km'):
    if direction == 'km-mi':
        return distance / 0.1093
    else:
        return distance * 1.6093


def CheckNumeric(wzone,wcheck = 'INT', wmode = ''):
    try:
        if (wcheck == 'INT' or wcheck == 'integer' or wcheck == 'INTEGER' or wcheck == 'int'):
            wzone_numeric = int(wzone)
        elif (wcheck == 'FLOAT' or wcheck == 'float'):
            wzone_numeric = float(wzone)
        if (wmode == 'NOT-ZERO' and wzone_numeric <= 0):
            return False
        return True
    except:
        return False

def convNumeric(wzone,wcheck = 'FLOAT', wmode = '', default=0.0):

    wzone_numeric = default

    try:
        if (wcheck == 'INT' or wcheck == 'integer' or wcheck == 'INTEGER' or wcheck == 'int'):
            wzone_numeric = int(wzone)
        elif (wcheck == 'FLOAT' or wcheck == 'float'):
            wzone_numeric = float(wzone)
        elif (wcheck == 'LONG' or wcheck == 'long'):
            wzone_numeric = long(wzone)
        if (wmode == 'NOT-ZERO' and wzone_numeric <= 0):
            wzone_numeric =  0
        return wzone_numeric
    except:
        return default



#========================================================
#=== Capitalize Sentence separated by  blank or dash ====
#========================================================
def capitalizeString(rawString):
    if rawString:
        if string.find(rawString,' ') >= 0:
            rawString = subCapitalize(rawString,' ')
        elif string.find(rawString,'-') >= 0:
            rawString = subCapitalize(rawString,'-')
        elif string.find(rawString,'_') >= 0:
            rawString = subCapitalize(rawString,'_')
        else:
            rawString = rawString.capitalize()
    return rawString

def subCapitalize(rawString,sep):
    " execute Capitalize for each  Word "
    tabSubChar = string.split(rawString,sep)
    tabCharOut  = []
    for partString in tabSubChar:
        partString = partString.capitalize()
        tabCharOut.append(partString)
    rawString = string.join(tabCharOut,sep)
    return rawString


def current_site_url():
    """Returns fully qualified URL (no trailing slash) for the current site."""
    from django.contrib.sites.models import Site
    current_site = Site.objects.get_current()
    currentUrl = current_site.domain
    if string.find(currentUrl, ':') >=0:
        arrayUrl = string.split(currentUrl,':')
        return arrayUrl[0], arrayUrl[1]
    return currentUrl, ''


def set_cookie(response, key, value, days_expire = 7):
    if days_expire is None:
        max_age = 365 * 24 * 60 * 60  #one year
    else:
        max_age = days_expire * 24 * 60 * 60
    expires = datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age), "%a, %d-%b-%Y %H:%M:%S GMT")
    response.set_cookie(key, value, max_age=max_age, expires=expires, domain=settings.SESSION_COOKIE_DOMAIN, secure=settings.SESSION_COOKIE_SECURE or None)


def storeCookies(keyName, valueName):
    """
    store Cookie with it's Key and Value
    """
    dicCookies = {}
    try:
        dicCookies['key'] = keyName
        dicCookies['value'] = valueName
    except:
        pass
    return dicCookies

def getCookies(request, keyName, defaultValue = None):
    """
    Return value for a Cookie Key
    """

    returnValue = None
    if defaultValue or defaultValue == '':
        returnValue = defaultValue

    if request.COOKIES.has_key(keyName):
        returnValue = request.COOKIES[keyName]
    return returnValue


def compareDic(currentDic, LastDic):
    """
    compare 2 Python dictionnary and return first Key/Value which differs
    """
    for eachKey in currentDic:
        currentValue = currentDic[eachKey]
        if eachKey in LastDic:
            lastValue  = LastDic[eachKey]
            if currentValue != lastValue:
                return eachKey
    return ''

def convertStrToDic(evalStrDic):
    try:
        return ast.literal_eval(evalStrDic)
    except:
        return {}


def checkDic(evalStrDic):
    try:
        test = ast.literal_eval(evalStrDic)
        return True
    except:
        return False


def truncMiddleString(zone,maxLen = 0, ellipsis = '...'):
    if zone and maxLen > 0:
        if len(zone) > maxLen:
            zone = extendTrunc(zone,maxLen) + extendTrunc(zone, maxLen, ellipsis = '', trunc = 'R')
    return zone

def truncate(zone,maxLen,trunc = 'L'):
    truncZone = zone
    if trunc ==  'L':
        truncZone = zone[:maxLen]
    else:
        truncZone = zone[len(zone)-maxLen:]
    return truncZone

def truncSmart(data, maxlen):
    data = (data[:75] + '...') if len(data) > 75 else data
    return data

def smart_truncate3(text, length=100, suffix='...'):
    """Truncates `text`, on a word boundary, as close to
    the target length it can come.
    """

    slen = len(suffix)
    pattern = r'^(.{0,%d}\S)\s+\S+' % (length-slen-1)
    if len(text) > length:
        match = re.match(pattern, text)
        if match:
            length0 = match.end(0)
            length1 = match.end(1)
            if abs(length0+slen-length) < abs(length1+slen-length):
                return match.group(0) + suffix
            else:
                return match.group(1) + suffix
    return text

def joinTruncZone(tabCumulZone, trunc = 'L', zone = '' , maxLen = 0):
    truncZone = ''
    if trunc == 'L':
        truncZone = string.strip(strUTF8(string.join(tabCumulZone,' ')))
    else:
        tabCumulZone.reverse()
        truncZone = string.strip(strUTF8(string.join(tabCumulZone,' ')))
    if truncZone == '' and maxLen > 0 :
        truncZone = truncate(zone,maxLen,trunc)
    return truncZone

def extendTrunc(zone,maxLen = 0, ellipsis  = '...', trunc = 'L'):
    " ===== try to reduce the string by word (Trunc (L) Left->Right (R) Right->Left ====="
    truncZone = zone
    cumulPart = -1
    validTrunc = None
    tabCumulZone = []

    #============================================================
    #==== Execute Trunc string if Lenght above nnn Characters ===
    #============================================================

    if zone and maxLen > 0:
        if len(zone) <= maxLen :
            return truncZone                  # === no trunc string ===

        if isSpecialUnicode(zone):
            unicodeName = toUTF8(zone)
            if string.find(unicodeName,' ') >=0:
                tabSplit = string.split(unicodeName,' ')
                #===== trunc from left to Right ====
                if trunc == 'L':
                    tabStart = 0
                    TabStep = 1
                    TabMax = len(tabSplit)
                else:
                    tabStart = len(tabSplit)-1
                    TabStep = -1
                    TabMax = -1
                #============================================
                # ==== loop on each word                 ====
                for i in range(tabStart,TabMax,TabStep):
                    partName = tabSplit[i]
                    tabCumulZone.append(partName)
                    cumulPart += 1
                    if len(string.join(tabCumulZone,' ')) >= maxLen:
                        validTrunc = 1
                        tabCumulZone.remove(partName)
                        truncZone = joinTruncZone(tabCumulZone,trunc,zone,maxLen)   # === join to obtain a safe truncated string ===
                        break
                if not validTrunc:
                    truncZone = joinTruncZone(tabCumulZone,trunc,zone,maxLen)   # === join to obtain a safe truncated string ===
            else:
                truncZone = truncate(zone,maxLen,trunc)
        else:
            truncZone = truncate(zone,maxLen,trunc)

    truncZone += ellipsis
    return truncZone

def isSpecialUnicode(zone):
    " check if Unicode string is enclosed Aliens Characters oke Indii, Japenese, ... above 128 "
    for car in zone:
        if car not in string.ascii_letters and car != '' and car != ' ' and car != '\n':
            return True

def convertLatin1ToUtf8(data):
    try:
        converted = data.decode('latin1').encode('utf-8')
        return converted
    except:
        return data


#===========================================
#=== extended Str() for UTF8 environment ===
def strUTF8(ReturnData):
    if not isinstance(ReturnData, basestring):
        ReturnData = str(ReturnData)
    else:
        try:
            ReturnData = ReturnData.encode('utf-8')
        except:
            ReturnData = str(ReturnData)
    return  ReturnData

def strUTF16(ReturnData):
    if not isinstance(ReturnData, basestring):
        ReturnData = str(ReturnData)
    else:
        try:
            ReturnData = ReturnData.encode('utf-16LE')
        except:
            ReturnData = str(ReturnData)
    return  ReturnData

def toUTF8(StrData):
    " ==== encode to UTF8 an scii string ====="
    if isinstance(StrData, basestring):
        default_encoding = sys.getdefaultencoding()
        if default_encoding == 'ascii':
            default_encoding = 'utf-8'
        if not isinstance(StrData, unicode):
            try:
                StrData = unicode(StrData, default_encoding, errors='ignore')
            except:
                pass

    return StrData

def extractFromList(currentList):
    try:
        for eachElement in currentList:
            return eachElement
    except:
        return currentList


def commonPaginator(request, application=''):
    """
    manage Pagination number
    """

    status_pagination = ''
    mode   = request.POST.get('mode','next')
    number_page  = request.POST.get('number','1')
    number_page = convNumeric(number_page, wcheck='INT')

    try:
        max_page = request.session[application]
    except:
        max_page = 1

    if mode == 'next':
        number_page += 1
        if number_page >= max_page:
            number_page = max_page
            status_pagination = 'last'
    else:
        number_page = number_page - 1
        if number_page <= 1:
            number_page = 1
            status_pagination = 'first'

    return number_page, status_pagination, max_page

def extractWithDelimiters(zone, sep):

    returnZone = ''
    sepStart = ''
    sepEnd = ''

    if sep == '(' or sep == ')':
        sepStart = '('
        sepEnd = ')'
    elif sep == '"':
        sepStart, sepEnd = '"'
    elif sep == '[' or sep == ']':
        sepStart = '['
        sepEnd = ']'
    elif sep == '{' or sep == '}':
        sepStart = '{'
        sepEnd = '}'
    elif sep == '<' or sep == '>':
        sepStart = '<'
        sepEnd = '>'


    if sepEnd and sepStart:
        if zone.find(sepStart) >=0 and zone.find(sepEnd) >=0:
            start = zone.find(sepStart)+1
            end = zone.find(sepEnd)
            returnZone = zone[start:end]

    return returnZone

def getSeparator(sep=None):

    if not sep:
        sepId = settings.HAYSTACK_SEP_ID
    else:
        sepId = sep

    sepList = settings.SEPARATOR.get(sepId)
    sepStart = sepList[0]
    sepEnd = sepList[1]
    return sepStart, sepEnd

def getRangeSelecteddate(mode):
    """
    get Range date for a given key Date  (used by  a couple of Servicie page / Event stat / Ratings stat / ...)
    we will return a fromdate used to delimit Search perimeter by a Query Filter "...DATE...__gt=fromdate"
    """

    # --------------------------------------
    # --- Define available Range Date    ---
    # --------------------------------------
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
    # --------------------------------------
    returnModeLabel = mode
    fromDate = '1900-01-01 00:00:00'

    if mode:
        if mode in dicStatConv:
            keyDate = dicStatConv[mode]
            (fromDate, toDate) = getDateRangeStamp(keyDate)
            returnModeLabel = dicStatConvlabel[mode]

    return fromDate, returnModeLabel



def getSystemParameters(application, key, mode='list', title='Select Your'):
    """
    Get system parameters (single or array of Values)
    "List" return a list  Mode for Forms combobox, "dic" return an array of dictionnary
    """
    from account.models import Parameters
    from collections import defaultdict

    if mode == 'list':
        returnList = defaultdict(list)
    else:
        returnList = []
    ctrvalue = 0

    # -----------------------------------------------------
    # -- Invite selector in top of List Select your .... --
    if mode == 'list' and title:
        titleInvite = '%s %s' % (title, key.lower().capitalize())

    # -----------------------------------------
    # --- Loop on Values                    ---
    if key and application:
        if mode == 'list' and title:
            returnList[application].append(('', titleInvite))
        ParmObject = Parameters.objects.filter(group=application, key=key, enable=True).order_by('sequence')
        if ParmObject:
            for eachValue in ParmObject:
                if mode == 'list':
                    returnBlock = (eachValue.value, eachValue.label)
                    returnList[application].append(returnBlock)
                else:
                    returnBlock = {'value' : eachValue.value, 'label' : eachValue.label}
                    returnList.append(returnBlock)
                ctrvalue += 1
        if mode == 'list':
            return returnList.get(application)
        else:
            return returnList
    return returnList



def getParameters(application='', key='', group='', static=False, flat=False, value=False):
    """
    Get  parameters
    """
    from account.models import Parameters, Application
    ParmObject = None
    ReturnValue= ''

    # -----------------------------------------
    # --- Loop on Values                    ---
    # -----------------------------------------

    if group and key and application:
        applicationObj = Application.objects.filter(application=application)

        # ---------------------------------------------------
        # --- Global application should exist (Mandatory) ---
        if applicationObj:
            ParmObject = Parameters.objects.filter(application=applicationObj[0],group=group, key=key, enable=True)

            # --------------------------------------
            # --- Lookup on Parameter Key object ---
            if ParmObject:

                # --- Flat / Static Information (textarea, paragraph, ...) ----
                if (flat or static) and not value:
                    ReturnValue =  ParmObject[0].description

                # --- return simpale text Value or Mysql record Object ----
                if (static or flat) and not value:
                    return ReturnValue
                else:
                    return ParmObject[0].value

    return ParmObject



def convDataModels(value, type):
    """
    Conv for Mysql data
    """
    if type == 'boolean':
        if value == '1' or value == True:
            return True
        else:
            return False


def getAdminUser():

    adminUser = []

    # -----------------------------------------
    # --extract Admin  record Object        ---
    # -----------------------------------------
    amdinObjList = settings.ADMIN_EMAIL_CONTACT['admin']
    for eachAdmin in amdinObjList:
        objAdmin = User.objects.filter(email=eachAdmin)
        if objAdmin:
            adminUser.append(objAdmin[0])

    return adminUser


