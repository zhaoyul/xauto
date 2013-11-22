#!/usr/bin/python

import calutil
import Julian
import time
import string

localZoneFile = 'posix/US/Pacific'
localZoneNum = 4

gmtZoneFile = 'posix/GMT'
gmtZoneNum = 25

winZoneDict = {}  # value is english string, then zoneinfo zone file
winZoneDict[0] = ('(GMT -12:00) Eniwetok, Kwajalein', 'posix/Pacific/Kwajalein', -12)
winZoneDict[1] = ('(GMT -11:00) Midway Island; Samoa', 'posix/Pacific/Samoa', -11)
winZoneDict[2] = ('(GMT -10:00) Hawaii', 'posix/US/Hawaii', -10)
winZoneDict[3] = ('(GMT -09:00) Alaska', 'posix/US/Alaska', -9)
winZoneDict[4] = ('(GMT -08:00) Pacific Time (US & Canada); Tijuana', 'posix/US/Pacific', -8)
winZoneDict[5] = ('(GMT -07:00) Arizona', 'posix/US/Arizona', -7)
winZoneDict[6] = ('(GMT -07:00) Mountain Time (US & Canada)', 'posix/US/Mountain', -7)
winZoneDict[7] = ('(GMT -06:00) Central America', 'posix/America/Costa_Rica', -6)
winZoneDict[8] = ('(GMT -06:00) Central Time (US & Canada)', 'posix/US/Central', -6)
winZoneDict[9] = ('(GMT -06:00) Mexico City', 'posix/America/Mexico_City', -6)
winZoneDict[10] = ('(GMT -06:00) Saskatchewan', 'posix/Canada/Saskatchewan', -6)
winZoneDict[11] = ('(GMT -05:00) Bogota, Lima, Quito', 'posix/America/Bogota', -5)
winZoneDict[12] = ('(GMT -05:00) Eastern Time (US & Canada)', 'posix/US/Eastern', -5)
winZoneDict[13] = ('(GMT -05:00) Indiana (East)', 'posix/US/East-Indiana', -5)
winZoneDict[14] = ('(GMT -04:00) Atlantic Time (Canada)', 'posix/Canada/Atlantic', -4)
winZoneDict[15] = ('(GMT -04:00) Caracas, La Paz', 'posix/America/Caracas', -4)
winZoneDict[16] = ('(GMT -04:00) Santiago', 'posix/America/Santiago', -4)
winZoneDict[17] = ('(GMT -03:30) Newfoundland', 'posix/Canada/Newfoundland', -3.5)
winZoneDict[18] = ('(GMT -03:00) Brasilia', 'posix/America/Sao_Paulo', -3)
winZoneDict[19] = ('(GMT -03:00) Buenos Aires, Georgetown', 'posix/America/Buenos_Aires', -3)
winZoneDict[20] = ('(GMT -03:00) Greenland', 'posix/America/Thule', -3)
winZoneDict[21] = ('(GMT -02:00) Mid-Atlantic', 'posix/Etc/GMT+2', -2)
winZoneDict[22] = ('(GMT -01:00) Azores', 'posix/Atlantic/Azores', -1)
winZoneDict[23] = ('(GMT -01:00) Cape Verde Is.', 'posix/Atlantic/Cape_Verde', -1)
winZoneDict[24] = ('(GMT) Casablanca, Monrovia', 'posix/Africa/Casablanca', 0)
winZoneDict[25] = ('(GMT) Greenwich Mean Time: Dublin, London', 'posix/Europe/London', 0)
winZoneDict[26] = ('(GMT +01:00) Amsterdam, Berlin, Rome', 'posix/Europe/Stockholm', 1)
winZoneDict[27] = ('(GMT +01:00) Belgrade, Prague, Budapest', 'posix/Europe/Prague', 1)
winZoneDict[28] = ('(GMT +01:00) Brussels, Copenhagen, Madrid, Paris', 'posix/Europe/Paris', 1)
winZoneDict[29] = ('(GMT +01:00) Sarajevo, Warsaw, Zagreb', 'posix/Europe/Warsaw', 1)
winZoneDict[30] = ('(GMT +01:00) West Central Africa', 'posix/Etc/GMT-1', 1)
winZoneDict[31] = ('(GMT +02:00) Athens, Istanbul, Minsk', 'posix/Europe/Athens', 2)
winZoneDict[32] = ('(GMT +02:00) Bucharest', 'posix/Europe/Bucharest', 2)
winZoneDict[33] = ('(GMT +02:00) Cairo', 'posix/Africa/Cairo', 2)
winZoneDict[34] = ('(GMT +02:00) Harare, Pretoria', 'posix/Africa/Harare', 2)
winZoneDict[35] = ('(GMT +02:00) Helsinki, Riga, Tallinn', 'posix/Europe/Helsinki', 2)
winZoneDict[36] = ('(GMT +02:00) Jerusalem', 'posix/Asia/Jerusalem', 2)
winZoneDict[37] = ('(GMT +03:00) Baghdad', 'posix/Asia/Baghdad', 3)
winZoneDict[38] = ('(GMT +03:00) Kuwait, Riyadh', 'posix/Asia/Kuwait', 3)
winZoneDict[39] = ('(GMT +03:00) Moscow, St. Petersburg, Volgograd', 'posix/Europe/Moscow', 3)
winZoneDict[40] = ('(GMT +03:00) Nairobi', 'posix/Africa/Nairobi', 3)
winZoneDict[41] = ('(GMT +03:30) Tehran', 'posix/Asia/Tehran', 3.5)
winZoneDict[42] = ('(GMT +04:00) Abu Dhabi, Muscat', 'posix/Asia/Muscat', 4)
winZoneDict[43] = ('(GMT +04:00) Baku, Tbilisi, Yerevan', 'posix/Asia/Baku', 4)
winZoneDict[44] = ('(GMT +04:30) Kabul', 'posix/Asia/Kabul', 4.5)
winZoneDict[45] = ('(GMT +05:00) Ekaterinburg', 'posix/Asia/Yekaterinburg', 5)
winZoneDict[46] = ('(GMT +05:00) Islamabad, Karachi, Tashkent', 'posix/Asia/Karachi', 5)
winZoneDict[47] = ('(GMT +05:30) Calcutta, Chennai, Mumbai, New Delhi', 'posix/Asia/Calcutta', 5.5)
winZoneDict[48] = ('(GMT +05:45) Kathmandu', 'posix/Asia/Katmandu', 5.75)
winZoneDict[49] = ('(GMT +06:00) Almaty, Novosibirsk', 'posix/Asia/Almaty', 6)
winZoneDict[50] = ('(GMT +06:00) Astana, Dhaka', 'posix/Asia/Dhaka', 6)
winZoneDict[51] = ('(GMT +06:00) Sri Jayawardenepura', 'posix/Etc/GMT-6', 6)
winZoneDict[52] = ('(GMT +06:30) Rangoon', 'posix/Asia/Rangoon', 6.5)
winZoneDict[53] = ('(GMT +07:00) Bangkok, Hanoi, Jakarta', 'posix/Asia/Bangkok', 7)
winZoneDict[54] = ('(GMT +07:00) Krasnoyarsk', 'posix/Asia/Krasnoyarsk', 7)
winZoneDict[55] = ('(GMT +08:00) Beijing, Chongqing, Hong Kong, Urumqi', 'posix/Asia/Hong_Kong', 8)
winZoneDict[56] = ('(GMT +08:00) Irkutsk, Ulaan Bataar', 'posix/Asia/Irkutsk', 8)
winZoneDict[57] = ('(GMT +08:00) Kuala Lumpur, Singapore', 'posix/Asia/Singapore', 8)
winZoneDict[58] = ('(GMT +08:00) Perth', 'posix/Australia/Perth', 8)
winZoneDict[59] = ('(GMT +08:00) Taipei', 'posix/Asia/Taipei', 8)
winZoneDict[60] = ('(GMT +09:00) Osaka, Sapporo, Tokyo', 'posix/Asia/Tokyo', 9)
winZoneDict[61] = ('(GMT +09:00) Seoul', 'posix/Asia/Seoul', 9)
winZoneDict[62] = ('(GMT +09:00) Yakutsk', 'posix/Asia/Yakutsk', 9)
winZoneDict[63] = ('(GMT +09:30) Adelaide', 'posix/Australia/Adelaide', 9.5)
winZoneDict[64] = ('(GMT +09:30) Darwin', 'posix/Australia/Darwin', 9.5)
winZoneDict[65] = ('(GMT +10:00) Brisbane', 'posix/Australia/Brisbane', 10)
winZoneDict[66] = ('(GMT +10:00) Canberra, Melbourne, Sydney', 'posix/Australia/Sydney', 10)
winZoneDict[67] = ('(GMT +10:00) Guam, Port Moresby', 'posix/Pacific/Guam', 10)
winZoneDict[68] = ('(GMT +10:00) Hobart', 'posix/Australia/Hobart', 10)
winZoneDict[69] = ('(GMT +10:00) Vladivostok', 'posix/Asia/Vladivostok', 10)
winZoneDict[70] = ('(GMT +11:00) Magadan, Solomon Is., New Caledonia', 'posix/Asia/Magadan', 11)
winZoneDict[71] = ('(GMT +12:00) Auckland, Wellington', 'posix/Pacific/Auckland', 12)
winZoneDict[72] = ('(GMT +12:00) Fiji, Kamchatka, Marshall Is.', 'posix/Pacific/Fiji', 12)
winZoneDict[73] = ('(GMT +13:00) Nuku\'alofa', 'posix/Pacific/Tongatapu', 13)

def getTimeZoneNameList():
  "return a python list of timezone name strings"
  result = []
  for i in range(len(winZoneDict.keys())):
    crap = ('', '')
    zoneName = winZoneDict.get(i, crap)[0]
    result.append(zoneName)
  return result

def getTimeZoneDict():
  "return timezone dict"
  return winZoneDict

def getZoneFileFromZoneNumber(zoneNum):
  "given an integer, return the zonefile"
  crap = ('', '')
  zoneName, zoneNum, zoneOffset = winZoneDict.get(zoneNum, crap)
  return zoneNum

def getZoneNameFromZoneNumber(zoneNum):
  "given an integer, return the zone name"
  crap = ('', '', '')
  zoneName, zoneNum, zoneOffset = winZoneDict.get(zoneNum, crap)
  return zoneName

def getZonePosixFromZoneNumber(zoneNum):
  "given an integer, return the zone posix"
  zoneFile = getZoneFileFromZoneNumber(zoneNum)
  zonePosix = zoneFile.replace('posix/', '')
  return zonePosix

def getTimeDifference(zoneNum1, zoneNum2):
  """ returns the time difference between 2 timezones """
  zone1 = winZoneDict.get(zoneNum1)
  zone2 = winZoneDict.get(zoneNum2)
  if zone1 and zone2:
    return zone2[2] - zone1[2]
  return 0

def getGMTOffset(zoneNum):
  zoneName = getZoneNameFromZoneNumber(zoneNum)
  if string.find(zoneName,'-') < 0 and string.find(zoneName,'+') < 0:
    offset = 'GMT'
  else:
    offset = zoneName[1:11]
  offset = string.replace(offset, ":", "")
  offset = string.replace(offset, " ", "")
  return offset

def getUTC(zoneNum):
  zoneName = getZoneNameFromZoneNumber(zoneNum)
  if string.find(zoneName,'-') < 0 and string.find(zoneName,'+') < 0:
    UTC = '+0000'
  else:
    UTC = zoneName[1:11]
  UTC = string.replace(UTC, ":", "")
  UTC = string.replace(UTC, " ", "")
  UTC = string.replace(UTC, "GMT", "")
  
  return UTC
  
def getUTCWithColon(zoneNum):
  zoneName = getZoneNameFromZoneNumber(zoneNum)
  if string.find(zoneName,'-') < 0 and string.find(zoneName,'+') < 0:
    UTC = '+0000'
  else:
    UTC = zoneName[1:11]
  UTC = string.replace(UTC, " ", "")
  UTC = string.replace(UTC, "GMT", "")

  return UTC



def getZoneNumberFromOffset(offset):
  if int(offset) < 0:
    sign = '-'
  else:
    sign = '+'
  value = abs(int(offset))
  if value >= 100:
    offsetStr = '(GMT %s%.2d:%.2d)' % (sign, value/100, value%100)
  elif value >= 10:
    offsetStr = '(GMT %s%s:00)' % (sign, value)
  else:
    offsetStr = '(GMT %s0%s:00)' % (sign, value)
  
  if str(offset) == '0':
    offsetStr = '(GMT)'
    
  for i in range(len(winZoneDict.keys())):
    if winZoneDict[i][0].startswith(offsetStr):
      return i
  
  return None

def getUSZoneNameFromZoneNumber(zoneNum):
  if zoneNum == 4:
    return 'PT'
  elif zoneNum == 5 or zoneNum == 6:
    return 'MT'
  elif zoneNum == 8:
    return 'CT'
  elif zoneNum == 12:
    return 'ET'
  return ''


def getZoneNumberFromUSZoneName(zoneName):
  
  zoneName = string.upper(zoneName)
  
  if zoneName == 'PT' or zoneName == 'US/PACIFIC':
    return '4'
  elif zoneName == 'MT' or zoneName == 'US/MOUNTAIN':
    return '6'
  elif zoneName == 'CT' or zoneName == 'US/CENTRAL':
    return '8'
  elif zoneName == 'ET' or zoneName == 'US/EASTERN':
    return '12'
  return ''




def convertTimeTupleFromZoneToZone(timeTuple, oldZoneNum, newZoneNum):
  "convert time given zone integers"
  oldZoneFile = getZoneFileFromZoneNumber(oldZoneNum)
  newZoneFile = getZoneFileFromZoneNumber(newZoneNum)
  julianTime = Julian.Julian(timeTuple[0], timeTuple[1], timeTuple[2], timeTuple[3], timeTuple[4], timeTuple[5], oldZoneFile)
  julianTime.zone = newZoneFile
  return julianTime.timeTuple()

def convertMysqlTimestampFromZoneToZone(timestamp, oldZoneNum, newZoneNum):
  "convert time given zone integers"
  timeTupleOld = calutil.mysqlTimeStampToTimeTuple(timestamp)
  timeTupleNew = convertTimeTupleFromZoneToZone(timeTupleOld, oldZoneNum, newZoneNum)
  timestampNew = calutil.timeTupleToMysqlTimeStamp(timeTupleNew)
  return timestampNew

def convertTimeTupleFromUTCToZone(timeTuple, newZoneNum):
  "convert time given zone integers"
  return convertTimeTupleFromZoneToZone(timeTuple, 25, newZoneNum)

def convertMysqlTimestampFromUTCToZone(timestampUTC, newZoneNum):
  "convert time given zone integers"
  return convertMysqlTimestampFromZoneToZone(timestampUTC, 25, newZoneNum)

def convertTimeTupleFromZoneToUTC(timeTuple, oldZoneNum):
  "convert time given zone integers"
  return convertTimeTupleFromZoneToZone(timeTuple, oldZoneNum, 25)

def convertMysqlTimestampFromZoneToUTC(timestampZone, oldZoneNum):
  "convert time given zone integers"
  return convertMysqlTimestampFromZoneToZone(timestampZone, oldZoneNum, 25)

def convertTimeTupleFromZoneToZoneByFiles(timeTuple, oldZoneFile, newZoneFile):
  "convert time given zone files"
  julianTime = Julian.Julian(timeTuple[0], timeTuple[1], timeTuple[2], timeTuple[3], timeTuple[4], timeTuple[5], oldZoneFile)
  julianTime.zone = newZoneFile
  return julianTime.timeTuple()  

def convertTimeTupleToLocalTime(timeTuple, foreignZone):
  "given a 9-tuple time and a foreign time zone number, return local 9-tuple"
  return convertTimeTupleFromZoneToZone(timeTuple, foreignZone, localZoneNum)

def toInt(source, default = None):
  "convert source to int, or return default on conversion error"
  try:
    result = int(source)
  except (TypeError, ValueError, OverflowError):
    result = default
  return result

def exportTimeZoneMenuToPage(p, selectedNum = None, maxChar = 35):
  "add timezone menu to ClearSilver page HDF dataset"
  zoneDict = getTimeZoneDict()
  selectedInt = toInt(selectedNum, None)
  if selectedInt is None:
    selectedInt = localZoneNum # PST
  
  if selectedInt not in [12,8,6,4]: # ie the USA timezones
    p.setValue('mg.qdata.showallzones', 1)
  
  americanzones = ''
  for zone in [[12,'Eastern Time (USA)'],[8,'Central Time (USA)'],[6,'Mountain Time (USA)'],[4,'Pacific Time (USA)']]:
    if zone[0] == selectedInt:
      americanzones += '<option value="%s" selected>%s</option>' % (zone[0], zone[1])
    else:
      americanzones += '<option value="%s">%s</option>' % (zone[0], zone[1])

  allzones = ''
  for i in range(len(zoneDict.keys())):
    
    name = getZoneNameFromZoneNumber(i)
    if len(name) > maxChar:
      name = name[:maxChar] + "..."
  
    if i == selectedInt:
      allzones += '<option value="%s" selected>%s</option>' % (i, name)
    else:
      allzones += '<option value="%s">%s</option>' % (i, name)
  
  p.setValue('mg.qdata.allzones', allzones, isHtml=True, cleanHtml=False)
  p.setValue('mg.qdata.americanzones', americanzones, isHtml=True, cleanHtml=False)

def nowAtLocalZone():
  return time.localtime(time.time())

def nowAtTimeZone(nowZone = None):
  "return current time tuple in zone"
  if nowZone is None:
    nowZone = localZoneNum
  nowInLocalTime = time.localtime(time.time())
  result = convertTimeTupleFromZoneToZone(nowInLocalTime, localZoneNum, nowZone)
  return result

def nowAtTimeZoneByFile(newZoneFile):
  "return current time tuple in zone"
  nowInLocalTime = time.localtime(time.time())
  result= convertTimeTupleFromZoneToZoneByFiles(nowInLocalTime, localZoneFile, newZoneFile)
  return result

def thisTimeAtTimeZone(thisTuple, newZone = None):
  "convert this tuple from no zone to newZone"
  if newZone is None:
    newZone = localZoneNum
  zoneFile = getZoneFileFromZoneNumber(newZone)
  julianTime = Julian.Julian(thisTuple[0], thisTuple[1], thisTuple[2], thisTuple[3], thisTuple[4], thisTuple[5], zoneFile)
  return julianTime.timeTuple()

def timeTupleToLocalInt(timeTuple, zone):
  timeAtZone = thisTimeAtTimeZone(timeTuple, zone)
  timeLocal = convertTimeTupleToLocalTime(timeAtZone, zone)
  result = time.mktime(timeLocal)
  return result
