# coding=utf-8
from django.db import models
from django.conf import settings

from pagseguro import PagSeguro

from catalog.models import Product


class CartItemManager(models.Manager):

    def add_item(self, cart_key, product):

        # o metodo get_or_create ele retorna dois valores:
        # o primeiro valor e o item criado ou resgatado
        # e o segundo e um booleano se criou ou nao.
        if self.filter(cart_key=cart_key, product=product).exists():
            created = False
            cart_item = self.get(cart_key=cart_key, product=product)
            cart_item.quantity = cart_item.quantity + 1
            cart_item.save()
        else:
            created = True
            cart_item = CartItem.objects.create(
                cart_key=cart_key, product=product, price=product.price
            )

        return cart_item, created


class CartItem(models.Model):

    cart_key = models.CharField(

        'Chave do Carrinho', max_length=40, db_index=True

    )
    product = models.ForeignKey('catalog.Product', verbose_name='Produto')
    quantity = models.PositiveIntegerField('Quantidade', default=1)
    price = models.DecimalField('Preço', decimal_places=2, max_digits=10)

    objects = CartItemManager()

    class Meta:
        verbose_name = 'Item do Carrinho'
        verbose_name_plural = 'Itens dos Carrinhos'
        unique_together = (('cart_key', 'product'))

    def __str__(self):
        return '{} [{}]'.format(self.product, self.quantity)


class OrderManager(models.Manager):

    def create_order(self, user, cart_items):

        order = self.create(user=user)

        for cart_item in cart_items:
            order_item = OrderItem.objects.create(

                order=order, quantity=cart_item.quantity, product=cart_item.product,
                price=cart_item.price

            )
        return order


class Order(models.Model):

    STATUS_CHOICES = (

        # No codigo abaixo, o primeiro valor da tupla que vai ser armazenado no banco de dados
        # e o segundo, pode ser por exemplo colocado no formulario.
        (0, 'Aguardando Pagamento'),
        (1, 'Concluída'),
        (2, 'Cancelada'),

    )

    PAYMENT_OPTION_CHOICES = (

        ('deposit', 'Deposito'),
        ('pagseguro', 'PagSeguro'),
        ('paypal', 'Paypal'),

    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Usuário')
    status = models.IntegerField(
        'Situação', choices=STATUS_CHOICES, default=0, blank=True)
    payment_option = models.CharField(
        'Opção de pagamento', choices=PAYMENT_OPTION_CHOICES, max_length=20, default='deposit')
    # Nesse campo, ele pega a data atual em que o modelo  Order foi criado.
    created = models.DateTimeField('Criado em', auto_now_add=True)
    # Diferente do criado, o campo abaixo, tem a data atualizada, sempre em
    # que o objeto do modelo for alterado
    modified = models.DateTimeField('Modificado em', auto_now=True)

    objects = OrderManager()

    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'

    def __str__(self):
        return 'Pedido #{}'.format(self.pk)
    
    def products(self):
        products = []
        for item in self.items.all():
            products.append(item.product)
        return products

    def total(self):
        aggregate_queryset = self.items.aggregate(
            total = models.Sum(
                models.F('price') * models.F('quantity'),
                output_field=models.DecimalField()
            )
        )
        return aggregate_queryset['total']

    def pagseguro_update_status(self,status):
        if status =='3':
            self.status = 1
        elif status =='7':
            self.status = 2
        self.save()

    def pagseguro(self):
        pg = PagSeguro(
            email=settings.PAGSEGURO_EMAIL, token = settings.PAGSEGURO_TOKEN,
            config = {'sandbox': settings.PAGSEGURO_SANDBOX}
        )
        pg.sender = {
            'email': self.user.email
        }
        pg.reference_prefix = None
        pg.shipping = None
        pg.reference = self.pk

        for item in self.items.all():
            pg.items.append(
                {
                    'id': item.product.pk,
                    'description': item.product.name,
                    'quantity': item.quantity,
                    'amount': '%.2f' % item.price
                }
            )
        return pg


class OrderItem(models.Model):

    order = models.ForeignKey(
        Order, verbose_name='Pedido', related_name='items')
    product = models.ForeignKey('catalog.Product', verbose_name='Produto')
    quantity = models.PositiveIntegerField('Quantidade', default=1)
    price = models.DecimalField('Preço', decimal_places=2, max_digits=10)

    class Meta:
        verbose_name = 'Item do pedido'
        verbose_name_plural = 'Items dos pedidos'

    def __str__(self):
        return '[{}] {}'.format(self.order, self.product)



def post_save_cart_item(instance, **kwargs):

    if instance.quantity < 1:
        instance.delete()


models.signals.post_save.connect(

    post_save_cart_item, sender=CartItem, dispatch_uid='post_save_cart_item'

)
