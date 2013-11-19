#!/usr/bin/python

# calutil.py -- calendar utilities
#
# Guillaume Oneill <guillaume@eventbrite.com>
# 2010-10-09


import babel.dates
from babel.dates import format_date, format_datetime, format_time
import datetime
import math
import re
import string
import sys
import time
import timezoneutil
from datetime import datetime

libdate = {}
libdate ['FUTURE']              = '*'
libdate ['TODAY']               = '*'
libdate ['THIS WEEK']           = '*'
libdate ['NEXT WEEK']           = '*'
libdate ['THIS MONTH']          = '*'
libdate ['NEXT MONTH']          = '*'
libdate ['THIS YEAR']           = '*'
libdate ['NEXT YEAR']           = '*'
libdate ['WEEK']                = '*'
libdate ['MONTH']               = '*'
libdate ['YEAR']                = '*'
libdate ['YEAR TO DATE']        = '*'
libdate ['LAST7']               = '*'

libdate ['LAST7FROMYESTERDAY']  = '*'
libdate ['LASTWEEK']            = '*'
libdate ['LASTMONTH']           = '*'
libdate ['THISMONTH']           = '*'
libdate ['LASTYEAR']            = '*'
libdate ['LAST WEEK']           = '*'
libdate ['LAST MONTH']          = '*'
libdate ['LAST YEAR']           = '*'
libdate ['LASTYEAR']            = '*'
libdate ['PAST']                = '*'
libdate ['YESTERDAY']           = '*'
libdate ['DAY']                 = '*'
libdate ['ALL']                 = '*'
libdate ['YEAR TO DATE']        = '*'

libmonth = {}
libmonth ['JANUARY'] = '01'  # == january ==
libmonth ['FEBRUARY'] = '02'  # == february ==
libmonth ['MARCH'] = '03'  # == March ==
libmonth ['APRIL'] = '04'  # == April ==
libmonth ['MAY'] = '05'  # == May ==
libmonth ['JUNE'] = '06'  # == June ==
libmonth ['JULY'] = '07'  # ==  July ==
libmonth ['AUGUST'] = '08'  # == August ==
libmonth ['SEPTEMBER'] = '09'  # == september ==
libmonth ['OCTOBER'] = '10'  # == october ==
libmonth ['NOVEMBER'] = '11'  # == november ==
libmonth ['DECEMBER'] = '12'  # == December ==

generalDateFormat = '%Y-%m-%d'

#==============================================
#==============================================
#=== Compute duration between 2 Timestamp  ====
#=== accept only Positive duration   > 0   ====
#==============================================
#==============================================


def strUTF8(ReturnData):
    if not isinstance(ReturnData, basestring):
        ReturnData = str(ReturnData)
    else:
        try:
            ReturnData = ReturnData.encode('utf-8')
        except:
            ReturnData = str(ReturnData)
    return  ReturnData

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


def local_time_offset(t=None):
    "Return offset of local zone from GMT, either at present or at time t."

    if t is None:
        t = time.time()

    if time.localtime(t).tm_isdst and time.daylight:
        return -time.altzone
    else:
        return -time.timezone

def getCurrentGmtPosix(t = None):
    "Return Current Server in GMT Posix  +01:00,   -08:00"

    timezone = local_time_offset(t)
    timezone = str(timezone / 36)
    if timezone >= 0:
        currentGMT = '+%s:%s' % (timezone.zfill(4)[:2], timezone.zfill(4)[2:])
    else:
        currentGMT = '-%s:%s' % (timezone.zfill(4)[:2], timezone.zfill(4)[2:])
    return currentGMT

def CheckDiffDate(endDateTuple, startDateTuple):
    "Just Return diff Between end and Start in Millsecond"

    timef = time.mktime(endDateTuple)
    timei = time.mktime(startDateTuple)
    diff = timef - timei

    if diff < 0 :
        return False
    else:
        return True

def CurrentDateTuple9(selDate =  None):
    "== send current Date/time in 9 Tuple"
    DateFormat = '%Y-%m-%d %H:%M:%S'
    localDate = time.localtime()
    if selDate:
        localDate = selDate
    StartTime = time.strftime(DateFormat,localDate)    # === Cron Start  Time                               ===
    #StartTime = isoTimeStringToTuple(StartTime)
    return StartTime

#========================================================
#========================================================
#==== Conv to  Pacific Time                           ===
#========================================================
#========================================================

def ConvDateToTimezone(ObjEvent, selectedDate = None,tzoneNum= None,Reverse=None):
    "=== return Date with current Event's Timezone ==="

    if tzoneNum is None:
        tzoneNum = ObjEvent.timezone()

    cutOffTupleRaw = mysqlTimeStampToTimeTuple(selectedDate)  # == conv date to Tuple ===
    PacificTime = timezoneutil.localZoneNum                           # Current pacific Timezone
    EventTime = tzoneNum                                              # === Event Timezone

    if Reverse:
        cutOffAtEventTuple= timezoneutil.convertTimeTupleFromZoneToZone(cutOffTupleRaw,PacificTime,EventTime)    # === conv Pacific Time(Server) to Event Time ===
    else:
        cutOffAtEventTuple= timezoneutil.convertTimeTupleFromZoneToZone(cutOffTupleRaw,EventTime,PacificTime)    # === conv Event Time to pacific Time         ===

    DateTimezone = dateTimeAsIso8601(cutOffAtEventTuple)
    return DateTimezone

#================================================================================
#================================================================================
#===  C H E C K    A N D   R E T U R N    R A N G E  O F   T I M E S T A M P  ===
#===               F O R    A L L    E V E N T   S E A R C H                  ===
#===       R E T U R N      S T A R T   A N D   E N D   T I M E S T A M P     ===
#================================================================================
#================================================================================

def GetDateRangeForEvent(sel_date):
    "Check and compute Date Range for All Search Event by Specific date or range of date"

    if CheckYear(sel_date):
        sel_start_date,sel_end_date = getYearRange(sel_date)    # === Get start and end timeStamp ===
        return True,sel_start_date,sel_end_date,''

    elif CheckLibMonth(sel_date):
        sel_start_date,sel_end_date = getMonthRange(sel_date)    # === Get start and end timeStamp ===
        return True,sel_start_date,sel_end_date,''

    elif CheckDateRange(sel_date) :
        sel_start_date,sel_end_date = getDateRangeStamp(sel_date)    # === Get start and end timeStamp ===
        return True,sel_start_date,sel_end_date,''

    #================================================
    #=== Select a Date Range Start-End           ====
    #================================================

    elif string.find(sel_date,' ') >= 0:
        tab_date = string.split(sel_date,' ')
        sel_start_date = tab_date[0]
        sel_end_date = tab_date[1]
        #======================================
        #==== Start Date present (Tuple 0) ====
        if sel_start_date != '':
            MysqlStartTuple = CheckIsoDate(sel_start_date,'','','NO-TIME')          # ==  Check Start Date/Time ===
            if MysqlStartTuple == None:
                wmessage =' Invalid start date [ %s ] >>> Format (YYYY-MM-DD)'    % (sel_start_date)
                return False,None,None,wmessage
        #==================================
        #=== End date present tuple (1) ===
        if sel_end_date != '':
            MysqlEndTuple = CheckIsoDate(sel_end_date,'','','NO-TIME')              # ==  Check End Date/Time ===
            if MysqlEndTuple == None:
                wmessage =' Invalid start date [ %s ] >>> Format (YYYY-MM-DD)'    % (sel_end_date)
                return False,None,None,wmessage
        #=====================================================
        #=== We have 2 date in input ==> check if Diff > 0 ===
        if MysqlStartTuple and MysqlEndTuple:
            if (not  CheckDiffDate(MysqlEndTuple,MysqlStartTuple)):
                wmessage =' End date less than  start date [ %s > %s ] )'    % (sel_end_date,sel_start_date)
                return False,None,None,wmessage
        return True,sel_start_date,sel_end_date,''
    else:
        wmessage = 'Invalid Date  [ %s ]' % (sel_date)
        return False,None,None,wmessage

#======================================
#======================================
#=== Check Date Range              ====
#======================================
#======================================

def CheckDateRange(key,List = ''):
    "Check validity of Date Range"

    #============================================================
    #=== Date Range to be displayed are marked with a "D" =======
    libdate = {}
    key = string.upper(key)

    if List == '':
        return libdate.get(key)
    else:
        TabLisDate = []
        ListData = libdate.values()
        ListData.sort()
        for k in ListData:
            if k != '*':
                TabLisDate.append(k)
        return TabLisDate     # === just return a List of available Date Range ===

def CheckYear(Year):

    YearTuple = {}
    Wyear = string.upper(Year)

    for k in range(2037):
        if k<2001 or k >2037:
            continue
        YearTuple [str(k)] = k  # == 2008  ==
    return YearTuple.get(Wyear)

#======================================
#======================================
#=== Compute Total days in Month   ====
#======================================
#======================================

def CheckLibMonth(Wmonth,List=''):

    Wmonth = string.upper(Wmonth)

    if List == '':
        return libmonth.get(Wmonth)
    else:
        return libmonth         # == just return a List of available month ===

def getDateRange(key, timeTuple = None, current=None, dateFormat=generalDateFormat):
    "calculate the date range based on a key. returns week range by default"

    DateFormat = dateFormat
    key = string.upper(key)
    addDay = 0

    # ==================================================
    # === special case for one an entire given Month  ==
    if key in libmonth:
        currentYear = GetYear()
        currentMonth = libmonth[key]
        currentDate = "%s-%s-%s" % (currentYear, currentMonth, '01')
        timeTuple = mysqlTimeStampToTimeTuple(currentDate)
        beginTuple = getThisMonthStart(timeTuple)
        endTuple   = getMonthEnd(timeTuple)
        return beginTuple, endTuple

    #==================================================================================
    #=== Special case for LastNnn/ NextNnn (Last or Next  days - common procedure) ====
    if string.find(key,'LAST') >=0 :
        nbrDay = string.replace(key,'LAST','')         # === special case for LastNnn (Last Days) ===
        if CheckNumeric(nbrDay):
            lastDay = int(nbrDay)                        # === special case for LastNnn (Last Days) ===
            key = 'LAST'
    elif string.find(key,'NEXT') >=0 :
        nbrDay = string.replace(key,'NEXT','')         # === special case for LastNnn (Last Days) ===
        if CheckNumeric(nbrDay):
            lastDay = int(nbrDay)                        # === special case for LastNnn (Last Days) ===
            key = 'NEXT'



    if not timeTuple:
        if not current:
            addDay = 86400
        curtime = time.time() + addDay
        timeTuple = time.localtime(curtime)

    if key in ('DAY','TODAY'):
        beginTuple = getDayStart(timeTuple)
        endTuple   = getDayEnd(timeTuple)
    elif key == 'YESTERDAY':
        yesterday = time.mktime(timeTuple) - 86400
        yesTuple = time.localtime(yesterday)
        beginTuple = getDayStart(yesTuple)
        endTuple   = getDayEnd(yesTuple)
    elif key in ('WEEK', 'THIS WEEK'):
        beginTuple = getThisWeekStart(timeTuple)
        endTuple   = getThisWeekEnd(timeTuple)
    elif key in ('MONTH', 'THIS MONTH'):
        beginTuple = getThisMonthStart(timeTuple)
        endTuple   = getMonthEnd(timeTuple)
    elif key in ('YEAR', 'YEAR TO DATE','THIS YEAR'):
        beginTuple = getThisYearStart(timeTuple)
        endTuple   = getThisYearEnd(timeTuple)
    #===================================================================================
    #=== Common DateRange proc for All LASTnnn (nnn= nr of days, LAST7, LAST30, ...) ===
    elif key == 'LAST':
        beginTime = time.mktime(timeTuple) - (lastDay*86400)
        beginTuple = time.localtime(beginTime)
        endTuple   = timeTuple
    elif key == 'NEXT':
        beginTime = time.mktime(timeTuple) + (lastDay*86400)
        beginTuple = time.localtime(beginTime)
        endTuple   = timeTuple
    elif key == 'NEXT WEEK':
        (beginTuple,endTuple) = GetNextWeekStart()
    elif key == 'NEXT MONTH':
        (beginTuple,endTuple) = GetNextMonth()
    elif key == 'NEXT YEAR':
        (beginTuple,endTuple) = GetNextYear()
    elif key == 'LAST7FROMYESTERDAY':
        beginTime = time.mktime(timeTuple) - 8*86400
        beginTuple = time.localtime(beginTime)
        endTime = time.mktime(timeTuple) - 86400
        endTuple = time.localtime(endTime)
        return beginTuple, endTuple
    elif key in ('LASTWEEK', 'LAST WEEK'):
        beginTuple = getLastWeekStart(timeTuple)
        endTuple   = getLastWeekEnd(timeTuple)
    elif key in ('LASTMONTH', 'LAST MONTH'):
        beginTuple = getLastMonthStart(timeTuple)
        endTuple   = getLastMonthEnd(timeTuple)
    elif key in ('LASTYEAR', 'LAST YEAR'):
        beginTuple = getLastYearStart(timeTuple)
        endTuple   = getLastYearEnd(timeTuple)
    elif key in ('PAST'):
        beginTuple = time.strptime('2011-01-01',DateFormat)   # == start Date in the Past (default) ===
        endTuple   = getToday()                                              # == current Date                     ===
    elif key in ('FUTURE'):
        beginTuple   = getToday()                                            # == current Date                     ===
        endTuple = time.strptime('2099-01-01',DateFormat)     # == start Date in the Past (default) ===
    elif key in ('ALL'):
        beginTuple = time.gmtime(0)
        endTuple   = timeTuple
    else:
        beginTuple = getThisWeekStart(timeTuple)
        endTuple   = getThisWeekEnd(timeTuple)

    return beginTuple, endTuple


def getDateRangeStamp(key, timeTuple = None, current=None, dateFormat=generalDateFormat):
    "calculate the date range based on a key. returns week range by default"

    beginTuple, endTuple = getDateRange(key, timeTuple = timeTuple, current=current, dateFormat=dateFormat)
    try:
        if dateFormat == generalDateFormat:
            beginStamp = time.strftime('%Y-%m-%d 00:00:00', beginTuple)     #==== Begin TimeStamp ===
            endStamp   = time.strftime('%Y-%m-%d 23:59:59', endTuple)      #==== End TimeStamp   ===
        else:
            beginStamp = time.strftime(dateFormat, beginTuple)     #==== Begin TimeStamp ===
            endStamp   = time.strftime(dateFormat, endTuple)      #==== End TimeStamp   ===
    except:
        beginStamp =  beginTuple     #==== Begin TimeStamp ===
        endStamp   = endTuple        #==== End TimeStamp   ===

    return beginStamp, endStamp

def getTodayEnd(timeTuple):
    "return first day of week (monday) as time tuple"
    dayWeek = timeTuple[6]
    beginTime = time.mktime(timeTuple) - dayWeek * 86400
    endTime = beginTime + 7*86400
    return time.localtime(endTime)

def getThisWeekStart(timeTuple):
    "return first day of week (monday) as time tuple"
    dayWeek = timeTuple[6]
    beginTime = time.mktime(timeTuple) - dayWeek * 86400
    beginTuple = time.localtime(beginTime)
    return getDayStart(beginTuple)

def getThisWeekEnd(timeTuple):
    "return first day of week (monday) as time tuple"
    dayWeek = timeTuple[6]
    beginTime = time.mktime(timeTuple) - dayWeek * 86400
    endTuple = time.localtime(beginTime + 6*86400)
    return getDayEnd(endTuple)

def getLastWeekStart(timeTuple):
    "return first day of previous week (monday) as time tuple"
    beginTime = time.mktime(timeTuple) - 7*86400
    beginTuple = time.localtime(beginTime)
    return getThisWeekStart(beginTuple)

def getLastWeekEnd(timeTuple):
    "return first day of previous week (monday) as time tuple"
    endTime = time.mktime(timeTuple) - 7*86400
    endTuple = time.localtime(endTime)
    return getThisWeekEnd(endTuple)

def getThisMonthStart(timeTuple):
    "return first day of current month as time tuple"
    year = timeTuple[0]
    month = timeTuple[1]
    return (year, month, 1, 0, 0, 0, -1, 1, -1)

def getThisMonthEnd(timeTuple):
    "return last day of current month as time tuple"
    year = timeTuple[0]
    month = timeTuple[1] + 1
    if month == 13:
        month = 1
        year += 1
    return (year, month, 1, 0, 0, 0, -1, 1, -1)

def getLastMonthStart(timeTuple):
    "return first day of last month as time tuple"
    year = timeTuple[0]
    month = timeTuple[1] - 1
    if month == 0:
        month = 12
        year -= 1
    return (year, month, 1, 0, 0, 0, -1, 1, -1)

def getLastMonthEnd(timeTuple):
    "return last day of last month as time tuple"
    year = timeTuple[0]
    month = timeTuple[1]
    return (year, month, 1, 0, 0, 0, -1, 1, -1)

def getThisYearStart(timeTuple):
    "return first day of current year as time tuple"
    year = timeTuple[0]
    return (year, 1, 1, 0, 0, 0, -1, 1, -1)

def getThisYearEnd(timeTuple):
    "return last day of current year as time tuple"
    year = timeTuple[0] + 1
    return (year, 1, 1, 0, 0, 0, -1, 1, -1)

def getLastYearStart(timeTuple):
    "return first day of past year as time tuple"
    year = timeTuple[0] - 1
    return (year, 1, 1, 0, 0, 0, -1, 1, -1)

def getLastYearEnd(timeTuple):
    "return last day of past year as time tuple"
    year = timeTuple[0]
    return (year, 1, 1, 0, 0, 0, -1, 1, -1)


def getToday(wtime = '',wtuple = '',wformat='', withSeconds = 0):
    "return current date (by default ISO Date) or (Date under Tuple format) "

    #===================================
    #======= Return an ISO DATE ========
    if string.upper(wtuple) == 'NO' or string.upper(wtuple) == 'NOTUPLE' :
        if wformat == '':
            if wtime == '':
                if withSeconds:
                    CheckCurrentDate = '%Y-%m-%d %H:%M:%s'                      #== For checking if date >= Now     ==
                else:
                    CheckCurrentDate = '%Y-%m-%d %H:%M'                      #== For checking if date >= Now     ==
            else:
                CheckCurrentDate = '%Y-%m-%d'                            #== ISO date Format  yyy-mm-dd only ==
        else:
            CheckCurrentDate = wformat                               #== ISO date Format  user ==
        today = datetime.today()
        current_date = today.strftime(CheckCurrentDate)
        return current_date
    #===================================
    #==== return a Date Tuple        ===
    else:
        curtime = time.time()
        timeTuple = time.localtime(curtime)
        return timeTuple

def getMonthEnd(timeTuple):
    "return end of month as time tuple"
    if timeTuple[1] < 12:
        nextMonthStart = (timeTuple[0], timeTuple[1] + 1, 1, 0, 0, 0, -1, 1, -1)
    else:
        nextMonthStart = (timeTuple[0] + 1, 1, 1, 0, 0, 0, -1, 1, -1)
    result = time.localtime(time.mktime(nextMonthStart) - 1)
    return result


def GetYearMonth(YYYYMMDD = None, sep=None):
    " === return YearMonth from the given date"

    if not sep:
        FormatYear = "%Y%m"
    else:
        FormatYear = "%Y-%m"

    if YYYYMMDD:
        Seldate = YYYYMMDD
    else:
        Seldate =  datetime.datetime.now()
    CurrentYearMonth = Seldate.strftime(FormatYear)
    return CurrentYearMonth

def GetMonth(YYYYMMDD = None):
    " === return YearMonth from the given date"
    FormatYear = "%m"
    if YYYYMMDD:
        Seldate = YYYYMMDD
    else:
        Seldate =  datetime.datetime.now()
    CurrentMonth = Seldate.strftime(FormatYear)
    return CurrentMonth

def GetHourMn(YYYYMMDD = None):
    " === return YearMonth from the given date"
    FormatYear = "%H:%M"
    if YYYYMMDD:
        Seldate = YYYYMMDD
    else:
        Seldate =  datetime.datetime.now()
    currentTime = Seldate.strftime(FormatYear)
    return currentTime


def GetLibMonth(Wmonth,Long=''):

    WmoisTuple = {}

    WmoisTuple ['01'] = 'January'    #  == january ==
    WmoisTuple ['02'] = 'February'   # == february ==
    WmoisTuple ['03'] = 'March'      # == March ==
    WmoisTuple ['04'] = 'April'      # == April ==
    WmoisTuple ['05'] = 'May'        # == May ==
    WmoisTuple ['06'] = 'June'       # == June ==
    WmoisTuple ['07'] = 'July'       # ==  July ==
    WmoisTuple ['08'] = 'August'     # == August ==
    WmoisTuple ['09'] = 'September'  # == september ==
    WmoisTuple ['10'] = 'October'    # == october ==
    WmoisTuple ['11'] = 'November'   # == november ==
    WmoisTuple ['12'] = 'December'   # == December ==

    if WmoisTuple.get(Wmonth):
        wlibmonth = WmoisTuple.get(Wmonth)
        if Long != '':
            return wlibmonth
        else:
            return wlibmonth [0:3]

def MaxDayMonth(Wmonth,Wyear):

    WmoisTuple = {}
    WmoisTuple ['01'] = 31  # == january ==
    WmoisTuple ['02'] = 28  # == february ==
    WmoisTuple ['03'] = 31  # == March ==
    WmoisTuple ['04'] = 30  # == April ==
    WmoisTuple ['05'] = 31  # == May ==
    WmoisTuple ['06'] = 30  # == June ==
    WmoisTuple ['07'] = 31  # ==  July ==
    WmoisTuple ['08'] = 31  # == August ==
    WmoisTuple ['09'] = 30  # == september ==
    WmoisTuple ['10'] = 31  # == october ==
    WmoisTuple ['11'] = 30  # == november ==
    WmoisTuple ['12'] = 31  # == December ==

    if (Wmonth == '02'):
        try:
            Wyear = int(Wyear)
        except:
            maxdays = WmoisTuple.get(str(Wmonth))
            return maxdays
        #==== Year valid ====
        wdiv = int(Wyear / 4)
        if ((wdiv * 4) == Wyear):
            maxdays = 29
        else:
            maxdays = 28
    else:
        maxdays = WmoisTuple.get(str(Wmonth))


    return maxdays


def mysqlTimeStampToTimeTuple(mysqlTimeStampStr,selFormat = None):
    "given a mysql timestamp string, return a 9-tuple for use with time module"

    #========================================
    #=== ask for a specific format        ===
    if selFormat:
        try:
            return time.strptime(mysqlTimeStampStr, selFormat)
        except:
            mysqlTimeStampStr = convDatetimeToIsoDate(mysqlTimeStampStr)
            return time.strptime(mysqlTimeStampStr, selFormat)

    #====================================================
    #=== Try various Date Format                     ====
    try:
        return time.strptime(mysqlTimeStampStr, '%Y-%m-%d %H:%M:%S')
    except:
        pass

    try:
        return time.strptime(mysqlTimeStampStr, '%Y-%m-%d %H:%M')
    except:
        pass

    try:
        return time.strptime(mysqlTimeStampStr, '%Y-%m-%d')
    except:
        pass

def GetYear(YYYYMMDD = None):
    " === return Year from the given date"
    FormatYear = "%Y"
    if YYYYMMDD:
        Seldate = YYYYMMDD
    else:
        Seldate =  datetime.datetime.now()
    CurrentYear = int(Seldate.strftime(FormatYear))
    return CurrentYear


def dayDifference(startDate,endDate, convFormat = '%Y-%m-%d'):
    "   given 2 date in US format return diff in Days "
    try:
        startTime = time.mktime(time.strptime(startDate, convFormat))
        endTime = time.mktime(time.strptime(endDate, convFormat))
        dateDiff = round((endTime - startTime) / 86400, 0)
    except:
        dateDiff = 0

    return dateDiff


def convDatetimeToIsoDate(selDatetime, currentFormat = '%Y-%m-%d %H:%M'):

    try:
        current_date = selDatetime.strftime(currentFormat)
        return current_date
    except:
        return None



def convDateAsFormat(selDate,inputFormat,outputFormat):
    " Change Date Format "

    if selDate and inputFormat and outputFormat:
        try:
            timeTuple  = mysqlTimeStampToTimeTuple(selDate,inputFormat)
            return timeTupleToYYYYMMDD(timeTuple,Format = outputFormat)
        except:
            return SelFormat
    return


def timeTupleToYYYYMMDD(timeTuple = None,Format = None):
    "return time tuple as date string YYYY-MM-DD"
    if timeTuple is None:
        timeTuple = time.localtime(time.time())
    if Format:
        selFormat = Format
    else:
        selFormat = "%Y-%m-%d"
    result = time.strftime(selFormat, timeTuple)
    return result


def mysqlTimeStampToTimeTuple(mysqlTimeStampStr,selFormat = None):
    "given a mysql timestamp string, return a 9-tuple for use with time module"

    #========================================
    #=== ask for a specific format        ===
    if selFormat:
        try:
            return time.strptime(mysqlTimeStampStr, selFormat)
        except:
            mysqlTimeStampStr = convDatetimeToIsoDate(mysqlTimeStampStr, currentFormat=selFormat)
            return time.strptime(mysqlTimeStampStr, selFormat)

    #====================================================
    #=== Try various Date Format                     ====
    try:
        return time.strptime(mysqlTimeStampStr, '%Y-%m-%d %H:%M:%S')
    except:
        pass

    try:
        return time.strptime(mysqlTimeStampStr, '%Y-%m-%d %H:%M')
    except:
        pass

    try:
        return time.strptime(mysqlTimeStampStr, '%Y-%m-%d')
    except:
        pass


def convDatetimeToIsoDate(selDatetime, currentFormat = '%Y-%m-%d %H:%M'):

    try:
        current_date = selDatetime.strftime(currentFormat)
        return current_date
    except:
        return None


def computeFilterByDate(dateposted , mode='LAST', defaultDate=None, dateFormat='%Y-%m-%d %H:%M:%S'):
    """
    Compute date range for Search by date posted / ending time / ... (use within xxx days)
    """

    if mode =='LAST':
        dateStart = '1900-01-01 00:00:00'
    else:
        if not defaultDate:
            dateStart = '2199-01-01 00:00:00'
        else:
            dateStart = defaultDate

    if dateposted:
        dateposted = string.replace(dateposted, 'Any', '')
        dateposted = string.replace(dateposted, 'All', '')
        if dateposted:
            dateposted = string.split(dateposted, ' ')
            dateposted = dateposted[1]
            if CheckNumeric(dateposted):
                if dateposted == '24':
                    dateposted = 1
                dateRange = '%s%s' % (string.upper(mode), dateposted)
                (dateStart, dateEnd)  = getDateRangeStamp(dateRange, current=1, dateFormat=dateFormat)

    return dateStart


def getDayStart(timeTuple):
  "return beginning of day as time tuple"
  return (timeTuple[0], timeTuple[1], timeTuple[2], 0, 0, 0, -1, 1, -1)


def getDayEnd(timeTuple):
  "return end of day as time tuple"
  return (timeTuple[0], timeTuple[1], timeTuple[2], 23, 59, 59, -1, 1, -1)










