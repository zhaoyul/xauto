from project.settings import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

SOCKET_STREAMER_URL = "/photostream"
SOCKET_STREAMER_PORT = 49002
SOCKET_STREAMER_FULL_URL = "http://localhost:%i%s" % (SOCKET_STREAMER_PORT, SOCKET_STREAMER_URL)

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

STATIC_URL = '/app/static/'

ROOT_URLCONF = 'project.dev_urls'
