from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.views.generic import list_detail
from bm.client.RPCQuerySet import RPCQuerySet
from django.contrib.auth.views import login as generic_login
from django.contrib.auth.decorators import login_required
from django.template.loader import select_template
from django.contrib.auth.forms import UserCreationForm
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login as user_login
from django.forms import fields
from bm.client.forms import RegistrationForm, MessageForm, LoginForm

MENU = ( ('Origin','bm.client.views.index'), 
         ('My Battles','bm.client.views.player_stats'), 
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
        
    return generic_login(request, template_name='login.html', authentication_form=LoginForm)

@login_required
def player_stats(request, part = None):
    if part == "details":
        pass
    else:
        object = "Battle"
        queryset = RPCQuerySet("PlayerBattle", params=[request.user.id])
        
    return list_detail.object_list(request, queryset, template_name="list.html", extra_context={'object_name':object})

@login_required
def messages(request):
    object = "Message"
    queryset = RPCQuerySet(object, request=request, params=[False])
    return list_detail.object_list(request, queryset, template_name="messages.html", extra_context={'object_name':object})

@login_required
def messages_send(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            queryset = RPCQuerySet("Message", request = request)
            queryset.sendRequest("sendMessage", form.cleaned_data["user_to"]["id"], form.cleaned_data["subject"], form.cleaned_data["message"])

            return HttpResponseRedirect(reverse("bm.client.views.messages"))
    else:
        form = MessageForm(initial = request.GET)
    
    return render_to_response("compose.html", {
        'form' : form
    }, context_instance=RequestContext(request))

@login_required
def messages_read(request, id):
    return detail(request, "Message", id, True)

@login_required
def messages_delete(request, id):
    queryset = RPCQuerySet("Message", request = request)
    queryset.sendRequest("deleteMessage", id)
    return HttpResponseRedirect(reverse("bm.client.views.messages"))

def maps(request):
    object = "Map"
    queryset = RPCQuerySet("Map")
        
    return list_detail.object_list(request, queryset, template_name="list.html", extra_context={'object_name':object})

def shop(request):
    object = "ShipModel"
    queryset = RPCQuerySet(object)
        
    return list_detail.object_list(request, queryset, template_name="list.html", extra_context={'object_name':object})

def stats(request, category = "player_rate"):
    
    if category == "player_rate":
        object = "Player"
        order_by = "-userprofile__reputation"
        category_title = "Top Rated Fighters"
    
    queryset = RPCQuerySet(object, params=[{}, order_by, 5])
        
    return list_detail.object_list(request, queryset, template_name="stats.html", extra_context={'object_name':object, "category":category_title})

def detail(request, object, id, auth = False):
    if object == "User":
        object = "Player"
    
    queryset = RPCQuerySet(object, request = request if auth else None)
    template = select_template(["detail/{0}.html".format(object), "detail.html",])    
    return list_detail.object_detail(request, queryset, object_id=id, template_name=template.name, extra_context={'object_name':object})

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            queryset = RPCQuerySet("User")
            queryset.rpc.createUser(form.cleaned_data["username"], form.cleaned_data["email"], form.cleaned_data["password1"])

            user = authenticate(username=form.cleaned_data["username"], password=form.cleaned_data["password1"])
            user_login(request, user)
            return HttpResponseRedirect(reverse("bm.client.views.player_stats"))
    else:
        form = RegistrationForm()

    return render_to_response("register.html", {
        'form' : form
    }, context_instance=RequestContext(request))
