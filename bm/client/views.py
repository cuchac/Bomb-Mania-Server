from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.views.generic import list_detail
from bm.client.RPCQuerySet import RPCQuerySet
from django.contrib.auth.views import login as generic_login
from django.contrib.auth.decorators import login_required

MENU = ( ('My Battles','bm.client.views.player_stats'), 
         ('Transmissions','bm.client.views.messages'), 
         ('Star Maps','bm.client.views.maps'),
         ('Space Docks','bm.client.views.shop'),
         ('Stats','bm.client.views.stats'),
         )

def index(request):
    
    context = {
        #"menu" : Menu(MENU),
    }
    
    return render_to_response("base_page.html", context_instance=RequestContext(request, context))

def login(request):
    if "username" in request.POST:
        request.session["username"] = request.POST["username"]
        request.session["password"] = request.POST["password"]
        
    return generic_login(request, template_name='login.html')

@login_required
def player_stats(request, part = None):
    if part == "oponents":
        pass
    else:
        queryset = RPCQuerySet("PlayerBattle", params=[request.user.id])
        
    return list_detail.object_list(request, queryset, template_name="list.html")

def messages(request):
    pass

def maps(request):
    pass

def shop(request):
    pass

def stats(request):
    pass

def detail(request, object, id):
    queryset = RPCQuerySet(object)
        
    return list_detail.object_detail(request, queryset, object_id=id, template_name="detail.html")