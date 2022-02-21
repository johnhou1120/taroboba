from django.shortcuts import render
from django.http.response import HttpResponse
from django.template.loader import get_template
# Create your views here.

def index(request):
    template = get_template('index.html')
    html = template.render(locals())
    return render(request, 'index.html', locals())

def menu(request):
    template = get_template('menu.html')
    html = template.render(locals())
    return render(request, 'menu.html', locals())