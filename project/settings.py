
# Django settings for project project.

import os

ADMINS = (
    ('Admin', 'admin@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'django-stub.db',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'UTC'
USE_TZ = True
# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en'

SITE_ID = 1

SITE_NAME = 'Xauto'

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(os.path.dirname(__file__), 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(os.path.dirname(__file__), 'static')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(os.path.dirname(__file__), 'xauto-front-end-master/build'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.DefaultStorageFinder',
    'compressor.finders.CompressorFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'fp!@p5(qne*cft+iw_72addfcaz#@pnoj=i8enwd7wh9r8'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'pagination.middleware.PaginationMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    'django.core.context_processors.tz',
    "django.core.context_processors.request",
    "django.contrib.messages.context_processors.messages",
)

ROOT_URLCONF = 'project.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    #os.path.join(os.path.dirname(__file__), "templates"),
)

INSTALLED_APPS = [
    'theme',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    #'django.contrib.flatpages',
    # Uncomment the next line to enable the admin:
    'grappelli',
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'django_extensions',
    'rest_framework',
    'rest_framework.authtoken',
    'sorl.thumbnail',
    'pagination',
    'registration',
    'south',
    'mailer',
    'compressor',
    'event',
    #'keywords',
    'multiuploader',
    #'member',
    'account',
    'docs',
    'xauto_lib',
    'storages',
    'socket_streamer',
    'timezone_field',
]

#EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
#EMAIL_BACKEND = 'django_mailer.smtp_queue.EmailBackend'
EMAIL_BACKEND = 'mailer.backend.DbBackend'

AUTHENTICATION_BACKENDS = (
    'email_login.auth_backend.EmailBackend',
    'django.contrib.auth.backends.ModelBackend',
    #'accounts.auth_backends.EmailAuthBackend',
)

#s3 settings
# DEFAULT_FILE_STORAGE = 'project.s3utils.MediaRootS3BotoStorage'
# AWS_ACCESS_KEY_ID = 'AKIAINTHBRGXXWEPYAXQ'
# AWS_SECRET_ACCESS_KEY = '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'
# AWS_STORAGE_BUCKET_NAME = 'xauto'

#django-registration settings
ACCOUNT_ACTIVATION_DAYS = 3
LOGIN_REDIRECT_URL = '/'


# -----------------------------------
# --- Event imaging
# -----------------------------------
# EVENT_IMAGES_ROOT = 'event_images/'
# MAX_EVENT_IMAGES = 2
# MAX_POPULAR_KEYWORD = 6
#
# GEOIP_PATH = os.path.join(os.path.dirname(__file__), 'apps', 'geoip2')
# GEOIP2_USER = 67594
# GEOIP2_KEY = 'qlJc88YJR1Ki'

DOCS_ROOT = os.path.join(os.path.dirname(__file__), '../docs/html')
DOCS_ACCESS = 'staff'

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

#django-compress settings
COMPRESS_ENABLED = False
COMPRESS_CACHE_BACKEND = 'locmem:///'

COUNTRIES_OVERRIDE = {
    "AF": None,
    "AX": None,
    "AL": None,
    "DZ": None,
    "AS": None,
    "AD": None,
    "AO": None,
    "AI": None,
    "AQ": None,
    "AG": None,
    "AM": None,
    "AW": None,
    "AZ": None,
    "BS": None,
    "BH": None,
    "BD": None,
    "BB": None,
    "BY": None,
    "BZ": None,
    "BJ": None,
    "BM": None,
    "BT": None,
    "BO": None,
    "BQ": None,
    "BA": None,
    "BW": None,
    "BV": None,
    "IO": None,
    "BN": None,
    "BF": None,
    "BI": None,
    "KH": None,
    "CM": None,
    "CV": None,
    "KY": None,
    "CF": None,
    "TD": None,
    "CL": None,
    "CX": None,
    "CC": None,
    "CO": None,
    "KM": None,
    "CG": None,
    "CD": None,
    "CK": None,
    "CR": None,
    "CI": None,
    "CU": None,
    "CW": None,
    "DJ": None,
    "DM": None,
    "DO": None,
    "EC": None,
    "SV": None,
    "GQ": None,
    "ER": None,
    "ET": None,
    "FK": None,
    "FO": None,
    "FJ": None,
    "GF": None,
    "PF": None,
    "TF": None,
    "GA": None,
    "GM": None,
    "GE": None,
    "GH": None,
    "GI": None,
    "GL": None,
    "GD": None,
    "GP": None,
    "GU": None,
    "GT": None,
    "GG": None,
    "GN": None,
    "GW": None,
    "GY": None,
    "HT": None,
    "HM": None,
    "VA": None,
    "HN": None,
    "IQ": None,
    "IM": None,
    "JM": None,
    "JE": None,
    "JO": None,
    "KZ": None,
    "KE": None,
    "KI": None,
    "KP": None,
    "KW": None,
    "KG": None,
    "LA": None,
    "LS": None,
    "LR": None,
    "LY": None,
    "LI": None,
    "MO": None,
    "MK": None,
    "MG": None,
    "MW": None,
    "MV": None,
    "ML": None,
    "MH": None,
    "MQ": None,
    "MR": None,
    "MU": None,
    "YT": None,
    "FM": None,
    "MD": None,
    "MC": None,
    "MN": None,
    "ME": None,
    "MS": None,
    "MA": None,
    "MZ": None,
    "MM": None,
    "NA": None,
    "NR": None,
    "NP": None,
    "NC": None,
    "NI": None,
    "NE": None,
    "NG": None,
    "NU": None,
    "NF": None,
    "MP": None,
    "PK": None,
    "PW": None,
    "PS": None,
    "PA": None,
    "PG": None,
    "PY": None,
    "PE": None,
    "PN": None,
    "PR": None,
    "RE": None,
    "RW": None,
    "BL": None,
    "SH": None,
    "KN": None,
    "LC": None,
    "MF": None,
    "PM": None,
    "VC": None,
    "WS": None,
    "SM": None,
    "ST": None,
    "SN": None,
    "RS": None,
    "SC": None,
    "SL": None,
    "SX": None,
    "SB": None,
    "SO": None,
    "GS": None,
    "SS": None,
    "LK": None,
    "SD": None,
    "SR": None,
    "SJ": None,
    "SZ": None,
    "SY": None,
    "TW": None,
    "TJ": None,
    "TZ": None,
    "TL": None,
    "TG": None,
    "TK": None,
    "TO": None,
    "TT": None,
    "TN": None,
    "TM": None,
    "TC": None,
    "TV": None,
    "UG": None,
    "UA": None,
    "UM": None,
    "UY": None,
    "UZ": None,
    "VU": None,
    "VE": None,
    "VG": None,
    "VI": None,
    "WF": None,
    "EH": None,
    "ZM": None,
    "ZW": None,
}

TOS_URL = u'#'
GOTO_BUTTON_URL=u'http://maps.apple.com/?q={lat},{lon}'

DATETIME_FORMAT = '%b %d, %Y'
APP_PREFIX = '/app'


# Default event image
DEFAULT_EVENT_IMAGE = '/static/images/default_pic.jpg'

# IMAGE SIZES
SMALL_THUMBNAIL_SIZE = u'50x36'  # used at my-events page
CARD_THUMBNAIL_SIZE = u'370x200'
HERO_THUMBNAIL_SIZE = u'1500x290'
ADMIN_THUMBNAIL_SIZE = u'60x60'
THUMBNAIL_SIZE = u'500x500'
PHOTOVIEWER_SIZE = u'1600x1200'


try:
    from settings_local import *
except Exception, err:
    import sys
    print >> sys.stderr, "Warning - Unable to import settings_local: %s" % err
