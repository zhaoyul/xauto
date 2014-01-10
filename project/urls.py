from django.conf.urls import *
from django.conf import settings


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.views.generic import RedirectView

admin.autodiscover()

js_info_dict = {
            #'packages':('photos', 'theme')
        }

urlpatterns = patterns('',
    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^grappelli/', include('grappelli.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^jsi18n/$', 'django.views.i18n.javascript_catalog', js_info_dict),
    #url(r'^settings/', include('livesettings.urls')),
    url(r'^documentation/', include('docs.urls')),
    url(r'^api/', include('api.urls')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
    #url(r'^auth/', include('auth.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^$', 'django.contrib.staticfiles.views.serve', {'path': '/index.html'}, name="index"),
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT}),
    )
else:
    urlpatterns += patterns('',
        url(r'^$', RedirectView.as_view(url='/'), name="index"),
    )