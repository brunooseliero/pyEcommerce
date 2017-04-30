from django.shortcuts import render
from django.http import HttpRequest
from django.http import HttpResponse
from catalog.models import Category


def index(request):
    return render(request, 'index.html')

def contact(request):
    return render(request, 'contact.html')

    #retirando essa view, pois ela foi para a aplicacao certa de catalogo, onde vai mostrar os produtos.

