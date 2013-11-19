from django.conf.urls import *
from account.views import account_view, testimonial
from account.views import customer_profile_view
from account.views import service_profile_view
from account.views import ad_alerts_view
from account.views import system_alerts_view, user_images_view, user_list_image, user_get_avatar, add_keyword, user_list_keywords, delete_keyword
from account.views import closeAccount, user_add_alert, user_list_alert, delete_alert, updateSystemAlert, getAccountStat


urlpatterns = patterns('',
    url(r'^testimonial/(?P<customer_id>\d+)/$', testimonial, name='testimonial'),
    url(r'^testimonial/(?P<customer_id>\d+)/(?P<origin>[-\w]+)/$', testimonial, name='testimonial_from'),
    url(r'^images/$', user_images_view, name='user-upload_images'),
    url(r'^user-images/(?P<user>\d+)/$', user_list_image, {'mode': 'account', 'application': 'team'}, name='user_list_images'),
    url(r'^user-avatar/(?P<user>\d+)/$', user_get_avatar, {'application': 'user'}, name='user_get_avatar'),
    url(r'^upload-keywords/(?P<user>\d+)/$', add_keyword, name='upload_keyword'),
    url(r'^user-keywords/(?P<user>\d+)/$', user_list_keywords, {'mode': 'account'}, name='user_list_keywords'),
    url(r'^user-alerts/(?P<user>\d+)/$', user_list_alert, {'mode': 'ad'}, name='user_list_alerts'),
    url(r'^delete-keywords/(?P<user>\d+)/$', delete_keyword, name='delete_keyword'),
    url(r'^get-account-stat/$', getAccountStat, name='account_buying_activity'),
    url(r'^close-account/$', closeAccount, name='close_account_request'),
)



