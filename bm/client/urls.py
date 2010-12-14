from django.conf.urls.defaults import patterns
from bm import settings

urlpatterns = patterns('',
    (r'^$', 'bm.client.views.index'),
    
    (r'^my_battles', 'bm.client.views.player_stats'),
    
    (r'^transmissions$', 'bm.client.views.messages'),
    (r'^transmissions/receive/(?P<id>[0-9]+)', 'bm.client.views.messages_read'),
    (r'^transmissions/delete/(?P<id>[0-9]+)', 'bm.client.views.messages_delete'),
    (r'^transmissions/transmit', 'bm.client.views.messages_send'),
    
    (r'^star_maps', 'bm.client.views.maps'),
    (r'^space_docks', 'bm.client.views.shop'),
    (r'^stats', 'bm.client.views.stats'),
    
    # Object details
    (r'^detail/(?P<object>[a-z_A-Z]+)/(?P<id>[0-9]+)', 'bm.client.views.detail'),
    
    # User login/logout
    (r'^login/$', 'bm.client.views.login'),
    (r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    (r'^new-fighter/$', 'bm.client.views.register'),

)

# Handle local file on debug server
if settings.DEBUG:
    urlpatterns += patterns('django.views.static',
    (r'^static/(?P<path>.*)$', 
        'serve', {
        'document_root': settings.MEDIA_ROOT,
        'show_indexes': True }),)