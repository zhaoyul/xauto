from django.conf.urls import *

urlpatterns = patterns('xauto.video.views',
    url(r'^preview/$', 'preview', name='youtube_preview'),
)
