from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.http import HttpResponse

def home(request):
    context = RequestContext(request)
    if request.user.is_authenticated():
        return render_to_response('home.html', context)
    return render_to_response('base.html', context)
