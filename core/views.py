from django.shortcuts import render
from django.http import HttpRequest
from django.http import HttpResponse
from catalog.models import Category
#import para o form de contato
from .forms import ContactForm


def index(request):
    #Definição da pagina Index
    #Rretornando a request e o template index.html.
    return render(request, 'index.html')

def contact(request):
    #Metodo para inicializar a pagina de contato
    #Se for um metodo Post, o objeto form reebe as informações que o usuário digitou. 
    if request.method == 'POST':
        form = ContactForm(request.POST)
        # se não, ele cria o form, passando um objeto form para o contexto da pagina html.
    else:
        form = ContactForm()
        context = {

            'form':form

        }       
    return render(request, 'contact.html', context)
    
    #retirando essa view, pois ela foi para a aplicacao certa de catalogo,
    # onde vai mostrar os produtos.

