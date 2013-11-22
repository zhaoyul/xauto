

# easterDay will only work for years between 1900 and 2099.
# It takes a year and gives the day and month for easterDay

EPOCH = 2440587L
SECSADAY = 86400L
HOURSADAY = 24L
MINUTESADAY = 1440L
SECSAHOUR = 3600L
SECSAMINUTE = 60L
MINUTESAHOUR = 60L
parts = ['year', 'month', 'day', 'hour', 'minute', 'second', 'time', 'julian', 'tz']


def easterDay(year):
  if year < 1900 or year > 2099:
    raise ValueError, 'easterDay is only valid from 1900 to 2099'
  year = int(year)
  a = year%19
  b = year%4
  c = year%7
  s = 19*a + 24
  d = s%30
  t = 2*b + 4*c + 6*d + 5
  e = t%7
  theDay = 22 + d + e
  if theDay >= 32:
    theMonth = 4
    theDay = d + e - 9
    if theDay == 26:
      theDay = 19
    elif theDay == 25 and a == 16 and d == 28:
      theDay = 18
  else:
    theMonth = 3
  return Julian(year, theMonth, theDay)


def julianDay(year, month, day):
  year, month, day = long(year), long(month), long(day)
  if month > 12L:
    year = year + month/12L
    month = month%12L
  elif month < 1L:
    month = -month
    year = year - month/12L - 1L
    month = 12L - month%12L
  if month < 3L:
    year = year - 1L
    month = month + 12L
# this is a problem for out of bounds dates...
  if year > 0L:
    yearCorr = 0L
  else:
    yearCorr = 3L
# this is a problem for out of bounds dates...
  if year*10000L + month*100L + day > 15821014L:
    b = 2L - year/100L + year/400L
  else:
    b = 0L
  return (1461L*year - yearCorr)/4L + 306001L*(month + 1L)/10000L + day + 1720994L + b

def calendarDayForJulian(julian):
  julian = long(julian)
  if (julian < 2299160L):
    b = julian + 1525L
  else:
    alpha = (4L*julian - 7468861L)/146097L
    b = julian + 1526L + alpha - alpha/4L
  c = (20L*b - 2442L)/7305L
  d = 1461L*c/4L
  e = 10000L*(b - d)/306001L
  day = int(b - d - 306001L*e/10000L)
  if e < 14L:
    month = int(e - 1L)
  else:
    month = int(e - 13L)
  if month > 2:
    year = c - 4716L
  else:
    year = c - 4715L
  return year, month, day

def now(zone=''):
  if not zone: zone = ''
  a = Julian(zone=zone)
  a.setToNow(zone=zone)
  return a

def julianFromString(dstr, format = ''):
  a = Julian()
  if format:
    a.formattedInput(dstr, format)
  else:
    a.parseInput(dstr)
  return a

class FakeZone:
  TZDIR = ''
  TZDEFAULT = 'GMT'
  def __init__(self, name = ''):
    self.name = self.TZDEFAULT

  def zone(self, name = ''):
    return self

  def zone_names(self):
    return [self.TZDEFAULT]

  def from_time(self, time):
    return time

  def info(self, time = 0):
    return 0, 0, self.TZDEFAULT

  def zones(self):
    return [self.TZDEFAULT]


class Julian:
  try:
    import Zone
    hasZone = 1
  except:
    Zone = FakeZone()
    hasZone = 0
  defaultZone = Zone.TZDEFAULT

  def __init__(self, year = None, month = None, day = None, hour = 0, minute = 0, second = 0, zone = ''):
    self.set(year, month, day, hour, minute, second, zone)

  def set(self, year = None, month = None, day = None, hour = 0, minute = 0, second = 0, zone = ''):
    if not zone:
      if hasattr(self, zone):
        zone = self.zone
      else:
        zone = self.defaultZone
    if day == None:
      try:
        del self.julian, self.year, self.month, self.day
        del self.hour, self.minute, self.second, self.tz, self.time
      except AttributeError:
        pass
      self.julian, self.year, self.month, self.day = EPOCH, 1970L, 1, 1
      self.hour, self.minute, self.second = 0, 0, 0
      self.tz = self.Zone.zone(zone)
      self.time = long(self.tz.from_time(0))
    else:
      self.setFromTime(self.Zone.zone(zone).from_time(SECSADAY*(julianDay(year, month, day) - EPOCH) + SECSAHOUR*long(hour) + SECSAMINUTE*long(minute) + long(second)), zone)

  def setFromJulian(self, jul, zone = ''):
    if not zone:
      if hasattr(self, zone):
        zone = self.zone
      else:
        zone = self.defaultZone
    self.setFromTime(self.Zone.zone(zone).from_time(SECSADAY*(long(jul) - EPOCH)), zone)

  def setFromTime(self, tval, zone = ''):
    if not zone:
      if hasattr(self, zone):
        zone = self.zone
      else:
        zone = self.defaultZone
    try:
      del self.julian, self.year, self.month, self.day
      del self.hour, self.minute, self.second, self.tz, self.time
    except AttributeError:
      pass
    self.tz = self.Zone.zone(zone)
    self.time = long(tval)
    seconds = self.time + self.tz.info(self.time)[0]
    self.julian = EPOCH + seconds/SECSADAY
    self.hour = int((seconds/SECSAHOUR)%HOURSADAY)
    self.minute = int((seconds/SECSAMINUTE)%MINUTESAHOUR)
    self.second = int(seconds%SECSAMINUTE)
    self.year, self.month, self.day = calendarDayForJulian(self.julian)

  def setToNow(self, zone = ''):
    import time
    self.setFromTime(time.time(), zone)

  def dayOfYear(self):
    return int(self.julian - julianDay(self.year, 1, 0))

  def dayOfWeek(self):
    return int((self.julian + 2L)%7L)

  def timeTuple(self):
    try:
      iyear = int(self.year)
    except:
      iyear = self.year
    return iyear, self.month, self.day, self.hour, self.minute, self.second, (self.dayOfWeek() - 1)%7, self.dayOfYear(), self.tz.info(self.time)[1]

  def __getattr__(self, name):
    if name == 'zone':
      return self.tz.name
    elif name in ('parseInput', 'formattedInput', 'formattedOutput', 'ap', 'tzAdjust', 'translatedFormat'):
      import JulianFormatting
      return getattr(self, name) 
    return self.__dict__[name]

  def __setattr__(self, name, value):
    if self.__dict__.has_key(name) and name in parts:
      if name == 'tz':
        raise AttributeError, name + ' is read only.  Set zone instead.'
      elif name == 'julian':
        (h, m, s) = (self.hour, self.minute, self.second)
        self.setFromJulian(value, self.zone)
        self.set(self.year, self.month, self.day, h, m, s, self.zone)
      elif name == 'time':
        self.setFromTime(value, self.zone)
      else:
        index = parts.index(name)
        st = [self.year, self.month, self.day, self.hour, self.minute, self.second, self.zone]
        st[index] = value
        apply(self.set, tuple(st))
    elif name == 'zone':
      self.setFromTime(self.time, value)
    else:
      self.__dict__[name] = value

  def __cmp__(self, other):
    if hasattr(other, 'time'):
      return cmp(self.time, other.time)
    return cmp(self.time, other)

  def __hash__(self):
    return hash(self.time)

  def __repr__(self):
    if self.__class__.__dict__.has_key('formattedOutput'):
      return self.formattedOutput()
    return `self.timeTuple()`

  def __add__(self, n):
    a = Julian()
    a.setFromTime(self.time + long(n), self.zone)
    return a

  __radd__ = __add__

  def __sub__(self, other):
    if hasattr(other, 'time'):
      return self.time - other.time
    return self + -other

  def __rsub__(self, other):
    raise TypeError, 'Julian can only be subtracted from other Julians.'

  def __getstate__(self):
    return self.time, self.zone

  def __setstate__(self, state):
    self.setFromTime(state[0], state[1])

  __members__ = ['year', 'month', 'day', 'hour', 'minute', 'second', 'zone', 'time', 'julian', 'tz']
  __methods__ = ['set', 'setFromJulian', 'setFromTime', 'setToNow', 'dayOfYear', 'dayOfWeek', 'timeTuple', 'formattedOutput', 'ap', 'tzAdjust', 'formattedInput', 'guessFormat', 'parseInput', 'translatedFormat']