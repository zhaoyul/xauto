import os
import datetime
import inspect

def _findNthCaller(n, frame):
  if n == 0:
    filename = inspect.getsourcefile(frame)
    line = inspect.getlineno(frame)
    return (filename, line)
  nextFrame = frame.f_back
  if not nextFrame:
    return ("<unknown>", 0)

  return _findNthCaller(n-1, nextFrame)


def findNthCaller(n):
  return _findNthCaller(n, inspect.currentframe().f_back)


class TaggedMessage(object):

  LEVELS = (
    (0, 'NOTSET'),
    (10, 'DEBUG'),
    (20, 'INFO'),
    (30, 'WARNING'),
    (40, 'ERROR'),
    (50, 'CRITICAL'),
  )

  created_at = None
  level = None
  code = None
  user_visible = False
  tags = {}
  message = None

  def __init__(self, message, level=10, code=None, user_visible=False, created_at=None, **kwargs):

    self.message = message
    for (k,v) in self.LEVELS:
      if level == v:
        level = k
      if level == k:
        break

    try:
      self.level = int(level)
    except ValueError:
      raise ValueError("Unknown level for log message: %s" % level)

    self.code = code
    self.user_visible = user_visible
    self.tags = kwargs
    if created_at is None:
      created_at = datetime.datetime.now()
    self.created_at = created_at

  def __repr__(self):
    parts = []
    parts.append(u'%s' % repr(self.message))
    if self.level != 10:
      parts.append(u'level=%s' % repr(self.level))
    if not self.code is None:
      parts.append(u'code=%s' % repr(self.code))
    if self.user_visible:
      parts.append(u'user_visible=True')
    parts.append(u'created_at=%s' % repr(self.created_at))
    parts.extend([u'%s=%s' % (key, repr(value)) for (key, value) in self.tags.iteritems()])
    r = u'%s(%s)' % (self.__class__.__name__, u', '.join(parts))
    return r

  def __unicode__(self):
    r = u''
    if len(self.tags) > 0:
      tagText = u", ".join([u'%s: %s' % (key, repr(value)) for (key, value) in self.tags.iteritems()])
      r += u'(%s) ' % tagText

    r += u'%s' % self.message
    return r

  def __str__(self):
    return unicode(self)


class Reporter(object):

  def say(self, message,  *args, **kwargs):

    tagged_message = TaggedMessage(message, *args, **kwargs)

    caller = findNthCaller(1)
    self.sayTagged(tagged_message, caller=caller)

  def sayTagged(self, tagged_message, caller=None, target=None):
    import logging
    if caller is None:
      caller = findNthCaller(1)
    if target is None:
      target = logging.getLogger()

    strMsg = u'%s:%d %s' % (os.path.basename(caller[0]) if caller[0] else '<unknown>', caller[1], unicode(tagged_message));
    target.log(tagged_message.level, strMsg)  