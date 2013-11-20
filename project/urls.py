from django.conf.urls import *
from django.conf import settings
from django.views.generic import TemplateView


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

js_info_dict = {
            #'packages':('photos', 'theme')
        }

urlpatterns = patterns('',
    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    #(r'^$', TemplateView.as_view(template_name="base.html")),
    #url('^$', ContestPhotoListView.as_view(), name="contestphoto_list"),
    #(r'^contest/', include('photos.urls')),
    #(r'^accounts/', include('registration.backends.default.urls')),
    #(r'^accounts/', include('accounts.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^jsi18n/$', 'django.views.i18n.javascript_catalog', js_info_dict),
    url(r'^settings/', include('livesettings.urls')),
    #url(r'^auth/', include('auth.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT}),
    )
