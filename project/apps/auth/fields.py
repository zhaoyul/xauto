import datetime
import base64
from django import forms
from django.utils.translation import ugettext_lazy as _

TIMESTAMP_DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S.%f'

class HoneypotField(forms.Field):
    def prepare_value(self, value):
        return None
    
class TimestampField(forms.Field):
    """
    Timestamp field to check last submit time and submiting's count in honeypot form.
    Format: '2013-04-26 14:15:32.338000|1', encoded with base64(encoding method can be changed, if need more security), where
    '2013-04-26 14:15:32.338000' - last submit time
    '1' - submiting's count
    """
    widget = forms.HiddenInput
    
    def prepare_value(self, value):
        if value is None:
            trying_count = 1
        else:
            try:
                value = base64.decodestring(value)
                trying_count = int(value.split('|')[1])
                trying_count += 1
            except: 
                trying_count = 1
        value = datetime.datetime.now().strftime(TIMESTAMP_DATETIME_FORMAT) + '|' + str(trying_count)
        value = base64.encodestring(value)
        return value
    
    def to_python(self, value):
        try:
            value = base64.decodestring(value)
            timestamp, trying_count = value.split('|')
            timestamp = datetime.datetime.strptime(timestamp, TIMESTAMP_DATETIME_FORMAT)
            trying_count = int(trying_count)
        except:
            raise forms.ValidationError(_('Invalid format.'))
        return (timestamp, trying_count)