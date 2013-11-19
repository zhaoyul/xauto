#!/usr/bin/python


import os
import sys
import time
from django.conf import settings

def tofile(filename, content, format='%Y-%m', clear = None):
  # Log content to a file:
  now = time.localtime(time.time())
  fullFilename = "%s%s_%s.log" % (settings.LOG_XAUTO_FILE, filename, time.strftime(format, now))
  
  try:
    if os.path.isfile(fullFilename):
      if clear:
        os.remove(fullFilename)
        f = open(fullFilename, 'w')
        f.write('%s - %s\n' % (time.strftime('%Y-%m-%d %H:%M:%S', now)[:19], content))
        f.close()
      else:
        f = open(fullFilename, 'a')
        f.write('%s - %s\n' % (time.strftime('%Y-%m-%d %H:%M:%S', now)[:19], content))
        f.close()
    else:
      f = open(fullFilename, 'w')
      f.write('%s - %s\n' % (time.strftime('%Y-%m-%d %H:%M:%S', now)[:19], content))
      f.close()
  except IOError:
    pass
