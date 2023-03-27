from django.shortcuts import render
from .models import Menu


def menu_view(request, menu_name):
    menu_items = Menu.objects.filter(name=menu_name)
    return render(request, 'menu.html', {'menu_items': menu_items})
