from django.conf.urls.defaults import patterns

urlpatterns = patterns('',
    (r'^$', 'bm.client.views.index'),
)
