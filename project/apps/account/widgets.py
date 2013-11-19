from django import forms
from django.forms.util import flatatt
from django.utils.safestring import mark_safe
from django.utils import datetime_safe

import datetime

DAY_CHOICES = [('%.2d' % d, '%.2d' % d) for d in range(1, 32)]
MONTH_CHOICES = [('%.2d' % d, '%.2d' % d) for d in range(1, 13)]

class BirthdayInput(forms.MultiWidget):
    """
    """
    def __init__(self, attrs=None, date_format=None, time_format=None):
        year_choices = [(y, y) for y in range(datetime.date.today().year - 17, 1930, -1)]
        widgets = (
            forms.Select(attrs=attrs, choices=DAY_CHOICES),
            forms.Select(attrs=attrs, choices=MONTH_CHOICES),
            forms.Select(attrs=attrs, choices=year_choices)
        )
        super(BirthdayInput, self).__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            return [value.day, value.month, value.year]
        return [None, None, None]
