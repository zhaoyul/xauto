# -*- coding: utf-8 -*-
from project.settings import *
DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Jakub Wisniowski', 'jwisniowski@milosolutions.com'),
    ('Mateusz Szefer', 'mszefer@milosolutions.com'),
    ('Maciej Zuk', 'mzuk@milosolutions.com'),
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', #, 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'xauto',                      # Or path to database file if using sqlite3.
        'USER': 'xauto',                      # Not used with sqlite3.
        'PASSWORD': 'xauto123',                  # Not used with sqlite3.
        'HOST': 'localhost',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '8442',                      # Set to empty string for default. Not used with sqlite3.
    }
}

#STATIC_ROOT = '/var/www/xauto.dev.milosolutions.com/static'
#MEDIA_ROOT = '/var/www/xauto.dev.milosolutions.com/media'

ALLOWED_HOSTS = ['xauto.dev2.milosolutions.com', 'www.xauto.dev2.milosolutions.com']

COMPRESS_ENABLED = True

INSTALLED_APPS = INSTALLED_APPS + [
    'gunicorn',
    'raven.contrib.django.raven_compat'
]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        }
    }
}

SOCKET_STREAMER_URL = "/photostream"
SOCKET_STREAMER_PORT = 8449
SOCKET_STREAMER_FULL_URL = "http://xauto.dev2.milosolutions.com:%i%s" % (SOCKET_STREAMER_PORT, SOCKET_STREAMER_URL)

FORCE_SCRIPT_NAME = '/app'

RAVEN_CONFIG = {
    'dsn': 'http://c78daee601974a69bfe4377165b675d8:50ac16cd6054469fa486fa6f6100400d@sentry.milosolutions.com/11',
}