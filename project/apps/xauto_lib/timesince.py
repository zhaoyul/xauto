import datetime
import time

from django.utils.tzinfo import LocalTimezone
from django.utils import dateformat
from django.utils.translation import ungettext

def timesince(d, now=None):
    """
    Xauto-style version of django.utils.timesince.
    
    Displays a single (lowest) relative time value, changing to absolute
    time over a preset limit.
    """
    chunks = (
      (60 * 60 * 24 * 365, lambda n: ungettext('year', 'years', n)),
      (60 * 60 * 24 * 30, lambda n: ungettext('month', 'months', n)),
      (60 * 60 * 24 * 7, lambda n : ungettext('week', 'weeks', n)),
      (60 * 60 * 24, lambda n : ungettext('day', 'days', n)),
      (60 * 60, lambda n: ungettext('hour', 'hours', n)),
      (60, lambda n: 'min'),
      (1, lambda n: 'sec')
    )

    # Convert datetime.date to datetime.datetime for comparison.
    if not isinstance(d, datetime.datetime):
        d = datetime.datetime(d.year, d.month, d.day)
    if now and not isinstance(now, datetime.datetime):
        now = datetime.datetime(now.year, now.month, now.day)

    if not now:
        if d.tzinfo:
            now = datetime.datetime.now(LocalTimezone(d))
        else:
            now = datetime.datetime.now()

    # ignore microsecond part of 'd' since we removed it from 'now'
    delta = now - (d - datetime.timedelta(0, 0, d.microsecond))

    if delta.days <= 2:
        since = delta.days * 24 * 60 * 60 + delta.seconds
        if since < 0:
            # d is in the future compared to now, stop processing.
            return u""
    
        for i, (seconds, name) in enumerate(chunks):
            count = since // seconds
            if count != 0:
                break
        s = '%(number)d %(type)s' % {'number': count, 'type': name(count)}
        return s + ' ago'

    else:
        if d.year == now.year:
            format = "M jS"
        else:
            format = "M jS Y"
        return dateformat.format(d, format)
