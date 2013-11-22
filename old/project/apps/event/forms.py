from django import forms

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
