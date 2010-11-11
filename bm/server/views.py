# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render_to_response

def index(request):
    context = {}
    
    context["testVar"] = ["Helo World!", "ahoj"]
    
    return render_to_response("server/base.html", context)