# coding=utf-8
from django.shortcuts import render
from django.http import HttpRequest
from django.http import HttpResponse
from catalog.models import Category
# import para o form de contato
from django.core.mail import send_mail
from .forms import ContactForm
from django.conf import settings


def index(request):
    # Definição da pagina Index
    # Rretornando a request e o template index.html.
    return render(request, 'index.html')


def contact(request):
    # Metodo para inicializar a pagina de contato
    # Se for um metodo Post, o objeto form reebe as informações que o usuário
    # digitou.
    # definindo uma variavel de sucesso.
    success = False
    #Na linha abaixo, sera verificado se o POST esta vazio ou com valores.
    form = ContactForm(request.POST or None)
    if form.is_valid():
        form.send_mail()
        # setando a variavel sucesso para true.
        success = True
    context = {

        'form': form,
        'success': success
    }
        # formando o contexto com o form e a mensagem de sucesso do e-mail
        # enviado ou nao.
    return render(request, 'contact.html', context)

    # retirando essa view, pois ela foi para a aplicacao certa de catalogo,
    # onde vai mostrar os produtos.
