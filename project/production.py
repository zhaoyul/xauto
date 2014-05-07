# -*- coding: utf-8 -*-
from project.settings import *
from S3 import CallingFormat
DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Jakub Wisniowski', 'jwisniowski@milosolutions.com'),
    ('Mateusz Szefer', 'mszefer@milosolutions.com'),
    ('Maciej Zuk', 'mzuk@milosolutions.com'),
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', 
        'NAME': 'xauto',
        'USER': 'xauto',      
        'PASSWORD': 'W64qgiuoC',
        'HOST': '127.0.0.1',
        'PORT': '',         
    }
}

#STATIC_ROOT = '/var/www/xauto.dev.milosolutions.com/static'
#MEDIA_ROOT = '/var/www/xauto.dev.milosolutions.com/media'

# AWS Storage setttings
DEFAULT_FILE_STORAGE = 'project.s3utils.MediaRootS3BotoStorage'
AWS_ACCESS_KEY_ID = 'AKIAINTHBRGXXWEPYAXQ'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'xauto'
AWS_CALLING_FORMAT = CallingFormat.SUBDOMAIN

MEDIA_URL = 'http://xauto.s3.amazonaws.com/media/'
STATIC_URL = '/app/static/'

ALLOWED_HOSTS = ['xauto.co', 'xauto.dev.milosolutions.com', 'www.xauto.dev.milosolutions.com', '54.187.65.140']

COMPRESS_ENABLED = True

INSTALLED_APPS = INSTALLED_APPS + [
    'gunicorn',
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
SOCKET_STREAMER_FULL_URL = "http://xauto.dev.milosolutions.com:%i%s" % (SOCKET_STREAMER_PORT, SOCKET_STREAMER_URL)
FORCE_SCRIPT_NAME = '/app'

