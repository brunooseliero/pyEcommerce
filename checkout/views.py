#coding=utf-8
from pagseguro import PagSeguro

from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import (
    RedirectView, TemplateView, ListView, DetailView
)
from django.forms import modelformset_factory
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse
from django.conf import settings
from django.http import HttpResponse

from catalog.models import Product

from .models import CartItem, Order

class CreateCartItemView(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        product = get_object_or_404(Product, slug=self.kwargs['slug'])
        if self.request.session.session_key is None:
            self.request.session.save()
        cart_item, created = CartItem.objects.add_item(
            self.request.session.session_key, product
        )
        if created:
            messages.success(self.request, 'Produto adicionado com sucesso')
        else:
            messages.success(self.request, 'Produto atualizado com sucesso')
        return reverse('checkout:cart_item')

class CartItemView(TemplateView):

    template_name = 'checkout/cart.html'

    def get_formset(self, clear=False):
        CartItemFormSet = modelformset_factory(
            CartItem, fields=('quantity',), can_delete=True, extra=0
        )
        session_key = self.request.session.session_key
        if session_key:
            if clear:
                formset = CartItemFormSet(
                    queryset=CartItem.objects.filter(cart_key=session_key)
                )
            else:
                formset = CartItemFormSet(
                    queryset=CartItem.objects.filter(cart_key=session_key),
                    data=self.request.POST or None
                )
        else:
            formset = CartItemFormSet(queryset=CartItem.objects.none())
        return formset

    def get_context_data(self, **kwargs):
        context = super(CartItemView, self).get_context_data(**kwargs)
        context['formset'] = self.get_formset()
        return context

    def post(self, request, *args, **kwargs):
        formset = self.get_formset()
        context = self.get_context_data(**kwargs)
        if formset.is_valid():
            formset.save()
            messages.success(request, 'Carrinho atualizado com sucesso')
            context['formset'] = self.get_formset(clear=True)
        return self.render_to_response(context)


class CheckoutView(LoginRequiredMixin, TemplateView):

    #Informando o template que vai ser usado
    template_name = 'checkout/checkout.html'

    # definindo a logica para o Get
    def get(self, request, *args, **kwargs):
        # recuperando o codigo da sessao do usuario
        session_key = request.session.session_key

        # verficando se existe uma sessao valida e objetos no carrinho de compra
        if session_key and CartItem.objects.filter(cart_key=session_key).exists():
            # filtra todos os itens do carrinho associados ao id da sessao
            cart_items = CartItem.objects.filter(cart_key=session_key)
            # cria um pedido
            order = Order.objects.create_order(
                user=request.user, cart_items=cart_items
            )
            cart_items.delete()
        else:
            # excecao para se nao tiver nehum item no carrinho de compras
            messages.info(request, 'Não há itens no carrinho de compras')
            return redirect('checkout:cart_item')
        response =  super(CheckoutView, self).get(request, *args, **kwargs)
        response.context_data['order'] = order
        return response

##View para listagem de pedidos dos usuarios
class OrderListView(LoginRequiredMixin, ListView):

    template_name = 'checkout/order_list.html'
    paginate_by = 10
    def get_queryset(self):
        #retorna apenas os pedidos do usuario que estiver logado
        return Order.objects.filter(user=self.request.user)

##criacao de uma view para detalhamento dos pedidos
class OrderDetailView(LoginRequiredMixin, DetailView):

    template_name = 'checkout/order_detail.html'
    
    ## filtro para que o usuario nao consiga acessar pedidos que nao sao dele
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

class PagSeguroView(LoginRequiredMixin, RedirectView):

    def get_redirect_url(self,*args,**kwargs):
        order_pk = self.kwargs.get('pk')
        order = get_object_or_404(
            Order.objects.filter(user=self.request.user), pk=order_pk
        )

        pg = order.pagseguro()
        
        pg.redirect_url = self.request.build_absolute_uri(
            reverse('checkout:order_detail', args=[order.pk])
        )
        pg.notification_url = self.request.build_absolute_uri(
            reverse('checkout:pagseguro_notification')
        )

        response = pg.checkout()
        return response.payment_url

@csrf_exempt
def pagseguro_notification(request):
    notification_code = request.POST.get('notificationCode', None)
    if notification_code:
        pg = PagSeguro(
            email=settings.PAGSEGURO_EMAIL, token=settings.PAGSEGURO_TOKEN,
            config={'sandbox': settings.PAGSEGURO_SANDBOX}
        )
        notification_data = pg.check_notification(notification_code)
        status = notification_data.status
        reference = notification_data.reference
        try:
            order = Order.objects.get(pk=reference)
        except Order.DoesNotExist:
            pass
        else:
            order.pagseguro_update_status(status)
            order.send_email_status(order)
    return HttpResponse('OK')


checkout = CheckoutView.as_view()

cart_item = CartItemView.as_view()

create_cartitem = CreateCartItemView.as_view()

order_list = OrderListView.as_view()

order_detail = OrderDetailView.as_view()

pagseguro_view = PagSeguroView.as_view()




