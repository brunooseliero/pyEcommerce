# coding=utf-8
from django.shortcuts import render, get_object_or_404

from .models import Product, Category
from django.views import generic


class ProductListView(generic.ListView):
    """
    O Django ja tem implementado uma classe para listaggem de objetos que tem
    os metodos ORMs implementados.
    Quando voce tem variaveis de contexto no  HTML, basta colocar o atributo
    context_object_name que ele vai achar esse contexto no html.
    No caso abaixo, eu nao preciso colocar, pois a minha variavel de contexto chama 
    product_list, o Django faz uma tentativa colocando o nome da classe e add um _list,
    como uma variavel de contexto html, se ele achar ele lista se nao, nao vai mostrar nada.
    """
    # identificando a modelo
    model = Product
    # template html a ser usado
    template_name = 'catalog/product_list.html'
    # atributo para habilitar a paginação do Django
    paginate_by = 3


product_list = ProductListView.as_view()


class CategoryListView(generic.ListView):
    # template html a ser usado
    template_name = 'catalog/category.html'
    # um nome referente a classe para identificar no template
    context_object_name = 'product_list'
    # atributo para habilitar a paginação do Django
    paginate_by = 3

    def get_queryset(self):
        # filtra os produtos, para cada categoria, utilizando o slug ue é um identificador unico
        return Product.objects.filter(category__slug=self.kwargs['slug'])
    
    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        # definino um contexto com a categoria atual, para aparecer no topo da pagina de uma 
        # categoria selecionada.
        context ['current_category'] = get_object_or_404(Category, slug=self.kwargs['slug'])
        return context

category = CategoryListView.as_view()


def product(request, slug):
    """
    Este metodo, é responsavel, para pesquisar apenas uma produto,
    que é pesquisado também pelo slug da URL.
    """
    # criação do objeto produto, que tem apenas uma posição.
    product = Product.objects.get(slug=slug)
    # criação de um contexto para acessar os atributos no html.
    context = {

        'product': product

    }
    # renderização do tempalte product.html junto com o contexto.
    return render(request, 'catalog/product.html', context)
