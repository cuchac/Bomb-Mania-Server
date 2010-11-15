from settings import *
from django.contrib.sessions.models import Session

#Server settings
AUTH_PROFILE_MODULE = 'server.UserProfile'

INSTALLED_APPS = INSTALLED_APPS+('bm.server', 'bm.django_xmlrpc',)

ROOT_URLCONF = 'bm.urls'

Session.objects.all().delete()