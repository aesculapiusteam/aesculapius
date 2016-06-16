from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.http import HttpResponse

def home(request):
    context = RequestContext(request)
    return render_to_response('index.html', context)
