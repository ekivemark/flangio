from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings
import os



def home_index(request):    
    context = {}
    return render_to_response('index.html', RequestContext(request, context,))