# coding=utf-8
from django.shortcuts import render
from django.http import HttpRequest
from django.http import HttpResponse
from catalog.models import Category
# import para o form de contato
from django.core.mail import send_mail
from .forms import ContactForm
from django.conf import settings
from django.views.generic import View, TemplateView, CreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse_lazy

# retitando os metodos e omplementando as class based views

User = get_user_model()

class IndexView(TemplateView):

    #metodo para tornar a classe IndexView 'chamavel'
    template_name = 'index.html'

index = IndexView.as_view()


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

class RegisterView(CreateView):

    form_class = UserCreationForm
    template_name = 'register.html'
    model = User
    success_url = reverse_lazy('index')

register = RegisterView.as_view()