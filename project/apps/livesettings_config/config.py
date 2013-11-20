from livesettings import *
from livesettings.models import Setting
from django.conf import settings
from django.utils.translation import ugettext_lazy as _


SITE_GROUP = ConfigurationGroup('SITE', 'Site Settings')
EVENT_GROUP = ConfigurationGroup('EVENT', 'Event Settings')
MEMBERT_GROUP = ConfigurationGroup('MEMBER', 'Member Settings')

config_register(
    PositiveIntegerValue(SITE_GROUP,
        'LOGIN_DAYS',
        description="How many days to keep members logged in for",
        default=21,
    )
)

config_register(
    PositiveIntegerValue(EVENT_GROUP,
        'NUMBER',
        description="Sequence Number for Creating a Uniq Event Id",
        default=1,
    )
)


config_register(
    PositiveIntegerValue(MEMBERT_GROUP,
        'NUMBER',
        description="Sequence Number for Creating a Uniq Member Id",
        default=1,
    )
)

config_register(
    StringValue(SITE_GROUP,
        'ALLOWED_HTML_TAGS',
        description="HTML tags permitted in rich text fields",
        default="p i strong b u a h1 h2 h3 blockquote br ul ol li",
    )
)

DISPLAY_GROUP = ConfigurationGroup('DISPLAY', 'Display Settings')

'''
config_register(
    StringValue(SITE_GROUP,
      'PAYPAL',
      description="Xauto Paypal Address",
      default=settings.PAYPAL_RECEIVER_EMAIL,
      )
  )
'''

config_register(
    StringValue(SITE_GROUP,
      'DEPARTEMENT',
      choices=[
          ('dept1', 'Department 1'),
          ('dept2', 'Department 2'),
          ('dept3', 'Department 3'),
          ('dept4', 'Department 4')
          ],
      description="Contact US - Department choice",
      help_text = 'Set your own department list for Contact Page',
      default='dept1',
      )
  )

