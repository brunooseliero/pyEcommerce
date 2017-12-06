# coding=utf-8
from django.shortcuts import render
from datetime import datetime, date
from django.http import HttpRequest
from django.http import HttpResponse
from catalog.models import Category
from checkout.models import Order, OrderItem
from django.db.models import Count
# import para o form de contato
from django.core.mail import send_mail
from .forms import ContactForm
from django.conf import settings
from django.views.generic import View, TemplateView, CreateView, ListView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages
import arrow
import json
from django.contrib.auth.mixins import LoginRequiredMixin

# retitando os metodos e omplementando as class based views

User = get_user_model()


class IndexView(TemplateView):

    # metodo para tornar a classe IndexView 'chamavel'
    template_name = 'index.html'


index = IndexView.as_view()


def contact(request):
    # Metodo para inicializar a pagina de contato
    # Se for um metodo Post, o objeto form reebe as informações que o usuário
    # digitou.
    # definindo uma variavel de sucesso.
    success = False
    # Na linha abaixo, sera verificado se o POST esta vazio ou com valores.
    form = ContactForm(request.POST or None)
    if form.is_valid():
        # se o form for valido, envia e-mail
        form.send_mail()
        # setando a variavel sucesso para true.
        success = True
    elif request.method == 'POST':
        # se o form estiver errado, vai aparecer uma mensagem de erro.
        messages.error(request, 'Form invalido!')
    context = {

        'form': form,
        'success': success
    }
        # formando o contexto com o form e a mensagem de sucesso do e-mail
        # semelhante ao req.setAtribute do java.

    return render(request, 'contact.html', context)

    # retirando essa view, pois ela foi para a aplicacao certa de catalogo,
    # onde vai mostrar os produtos.

    # retirando a view de registro e passando para aplicacao de contas


class ReportsView(TemplateView, LoginRequiredMixin):

    template_name = 'salesReport.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sales'] = self.allSales()
        return context

    def allSales(self):
        
        sales = []
        sales.append(Order.objects.filter(status=0).count())
        sales.append(Order.objects.filter(status=1).count())
        sales.append(Order.objects.filter(status=2).count())

        return sales
        
 
ReportsView = ReportsView.as_view()
