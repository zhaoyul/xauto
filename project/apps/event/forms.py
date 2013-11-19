from itertools import count
from string import lower

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.conf import settings
from django.forms.util import ErrorList
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe
from django.utils.encoding import StrAndUnicode
from django.forms.widgets import RadioFieldRenderer, RadioInput, Select
from django.forms.forms import BoundField
from django.utils.translation import ugettext_lazy as _

from member.models import  RecoveryQuestion
from xauto_utils.multiupload import *
from django.utils.html import conditional_escape, conditional_escape

from xauto_utils.logger import Reporter

reporter = Reporter()

class MessageAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(MessageAdminForm, self).__init__(*args, **kwargs)

        self.fields['removed_by'] = forms.ChoiceField(choices=(
                ('-1', '[Both]'),
                ('0', '[None]'),
                (self.instance.sender_id, self.instance.sender),
                (self.instance.recipient_id, self.instance.recipient),
            )
            , widget=forms.RadioSelect())
