from django.conf.urls.defaults import patterns

urlpatterns = patterns('',
    (r'', 'bm.django_xmlrpc.views.handle_xmlrpc'),
)
