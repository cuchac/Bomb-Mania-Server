from settings import *
from django.contrib.sessions.models import Session

# Django core settings
INSTALLED_APPS = INSTALLED_APPS+('bm.client',)

TEMPLATE_CONTEXT_PROCESSORS = TEMPLATE_CONTEXT_PROCESSORS+('bm.client.context_processors.menu',)

ROOT_URLCONF = 'bm.client.urls'


LOGIN_REDIRECT_URL = "/my_battles"
LOGIN_URL = '/login'

# Client settings
RPC_SERVER = "http://localhost:8001/xml-rpc/"
AUTHENTICATION_BACKENDS = ('bm.client.RPCQuerySet.RPCAuthBackend',)


#Session.objects.all().delete()