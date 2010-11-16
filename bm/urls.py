from django.conf.urls.defaults import patterns, include

from django.contrib import admin
from bm import settings
admin.autodiscover()

urlpatterns = patterns('',
    # Server
    (r'^xml-rpc/', include('bm.server.urls')),

    # Admin section
    (r'^admin/', include(admin.site.urls)),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
)

# Handle local file on debug server
if settings.DEBUG:
    urlpatterns += patterns('django.views.static',
    (r'^static/(?P<path>.*)$', 
        'serve', {
        'document_root': settings.MEDIA_ROOT,
        'show_indexes': True }),)