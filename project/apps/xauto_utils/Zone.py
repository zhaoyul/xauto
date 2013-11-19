# Author:  Ted Horst <ted_horst@il.us.swissbank.com>

# TZDIR hacks by Keith Waclena <k-waclena@uchicago.edu>
# http://www.lib.uchicago.edu/keith/

import os

candidates = ['/home/mollyguard/zoneinfo/',
	      '/usr/share/zoneinfo',
	      ]

if os.environ.has_key('TZDIR'):
	TZDIR = os.environ['TZDIR']
else:
	TZDIR = None
	for d in candidates:
		if os.path.isdir(d):
			TZDIR = d
			break
	if not TZDIR:
		raise IOError, (2, 'No such file or directory')
	del d

if os.environ.has_key('TZDEFAULT'):
	TZDEFAULT = os.environ['TZDEFAULT']
elif os.environ.has_key('TZ'):
	TZDEFAULT = os.environ['TZ']
else:
	TZDEFAULT = '/etc/localtime'

RESERVED = 32
zoneCache = {}


def zone(name = ''):
	if not name:
		name = TZDEFAULT
	if not zoneCache.has_key(name):
		zoneCache[name] = Zone(name)
	return zoneCache[name]

class Zone:
	def __init__(self, name = ''):
		import xdrlib
		if not name:
			name = TZDEFAULT

		if name[:6] == 'India/':  # fix alanb bug
			name = 'Indian/' + name[6:]

		self.name = name
		try:
			fd = open(os.path.join(TZDIR, name), 'rb')
		except IOError, reason:
			import handleexception 
			handleexception.HandleException("Unable to open %s" % (os.path.join(TZDIR, name))) 
			fd = open(os.path.join(TZDIR, "UTC" ), 'rb')
			
		tz = fd.read()
		fd.close()
		pos = RESERVED
		up = xdrlib.Unpacker(tz[pos:pos + 12])
		pos = pos + 12
		self.tzh_timecnt = up.unpack_int()
		self.tzh_typecnt = up.unpack_int()
		self.tzh_charcnt = up.unpack_int()
		up.reset(tz[pos:pos + 4*self.tzh_timecnt])
		pos = pos + 4*self.tzh_timecnt
		self.transition_times = []
		for i in range(self.tzh_timecnt):
			self.transition_times.append(up.unpack_int())
		self.type_indexes = tz[pos:pos + self.tzh_timecnt]
		pos = pos + self.tzh_timecnt
		data = tz[pos:pos + 6*self.tzh_typecnt]
		self.ttinfos = []
		for i in range(self.tzh_typecnt):
			up.reset(data[6*i:6*i + 4])
			self.ttinfos.append((up.unpack_int(), ord(data[6*i + 4]), ord(data[6*i + 5])))
		pos = pos + 6*self.tzh_typecnt
		allzones = tz[pos:pos + self.tzh_charcnt]
		self.zonelist = ['']*len(allzones)
		place = 0
		for i in range(len(allzones)):
			if allzones[i] == '\000':
				self.zonelist[place] = allzones[place:i]
				place = i + 1

	def default_index(self):
		if self.tzh_timecnt == 0:
			return 0
		for i in range(self.tzh_typecnt):
			if self.ttinfos[i][1] == 0:
				return i
		return 0

	def index(self, when = None):
		t_t = self.transition_times
		if when == None:
			import time
			when = time.time()
		if self.tzh_timecnt == 0:
			ind = (0, 0, 0)
		elif when < t_t[0]:
			i = self.default_index()
			ind = (i, ord(self.type_indexes[0]), i)
		elif when >= t_t[-1]:
			if self.tzh_timecnt > 1:
				ind = (ord(self.type_indexes[-1]), ord(self.type_indexes[-1]), ord(self.type_indexes[-2]))
			else:
				ind = (ord(self.type_indexes[-1]), ord(self.type_indexes[-1]), self.default_index())
		else:
			for i in range(self.tzh_timecnt - 1):
				if when < t_t[i + 1]:
					if i == 0:
						ind = (ord(self.type_indexes[0]), ord(self.type_indexes[1]), self.default_index())
					else:
						ind = (ord(self.type_indexes[i]), ord(self.type_indexes[i + 1]), ord(self.type_indexes[i - 1]))
					break
		return ind

	def info(self, when = None):
		ttind = self.ttinfos[self.index(when)[0]]
		return ttind[0], ttind[1], self.zonelist[ttind[2]]

	def from_time(self, otime):
		for i in self.index(otime):
			ftime = otime - self.ttinfos[i][0]
			if otime == ftime + self.info(ftime)[0]:
				break
		return ftime

	def zones(self):
		return filter(None, self.zonelist)

def _nest_list(list, prefix, zdir):
	import os
	lv = os.listdir(zdir)
	for a in lv:
		if os.path.isfile(zdir + a):
			list.append(prefix + a)
		elif os.path.isdir(zdir + a) and a != os.curdir and a != os.pardir:
			_nest_list(list, prefix + a + os.sep, zdir + a + os.sep)

def zone_names():
	zs = []
	_nest_list(zs, '', TZDIR)
	return zs
