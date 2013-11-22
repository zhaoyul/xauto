#!/usr/bin/python

# log.py -- logging text to the httpd access and error log files
#
# Alan Braverman <alanb@alanb.com>
# 2001-06-11

import os
import time
from django.conf import settings

def tofile(filename, content, format='%Y-%m', clear = None, mode='staging'):
  # Log content to a file:
  if mode == 'staging':
    logFile = settings.LOG_XAUTO_FILE
  else:
    logFile = settings.SITE_LOGGING_LOCAL

  now = time.localtime(time.time())
  fullFilename = "%s%s_%s.log" % (logFile, filename, time.strftime(format, now))

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

