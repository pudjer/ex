
from django.shortcuts import render
from .models import MenuItem, Menu


def menu_view(request, name):
    return render(request, 'menu.html',{'name':name})


def element_view(request, name):

    elem = MenuItem.objects.get(name=name)
    context = {'elem': elem }
    return render(request, 'elem.html', context)
