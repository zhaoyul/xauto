from django.conf.urls import *
from django.conf import settings

try:
    delete_url = settings.MULTI_FILE_DELETE_URL
except AttributeError:
    delete_url = 'multi_delete'

try:
    image_url = settings.MULTI_IMAGE_URL
except AttributeError:
    image_url = 'multi_image'

urlpatterns = patterns('',
    url(r'^/multi_delete/(\d+)/$', 'multiuploader.views.multiuploader_delete', name='delete_image'),
    url(r'^/multi/$', 'multiuploader.views.multiuploader', name='multi'),
    url(r'^/multi-ajax/$', 'multiuploader.views.multiuploader_ajax', name='multi_ajax'),
    url(r'^/multi_image/(\d+)/$', 'multiuploader.views.multi_show_uploaded', name='multi_image'),
    url(r'^/ajax-uploader/$', 'multiuploader.views.ajaxUploader', name='ajax_uploader'),
    url(r'^/ajax-listfiles/$', 'multiuploader.views.user_list_files', name='ajax_list_files'),
)


