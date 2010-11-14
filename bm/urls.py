from django.conf.urls.defaults import patterns, include

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Server
    (r'^xml-rpc/', include('bm.server.urls')),

    # Admin section
    (r'^admin/', include(admin.site.urls)),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    
    # Rest is client
    (r'^$', include('bm.client.urls')),
)
