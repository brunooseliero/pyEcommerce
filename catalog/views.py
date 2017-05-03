#coding=utf-8
from django.shortcuts import render

from .models import Product, Category


def product_list(request):
    #Metodo para retornar uma lista de produtos
    #Passsa um contexto para pagina, com um objeto chamado product_list, contendo todos os Produtos do banco de dados.
    context = {
        'product_list' : Product.objects.all(),
    }
    #função para renderizar o template product_list.html junto com o contexto definido acima. 
    return render(request, 'catalog/product_list.html', context)

def category(request, slug):
    """
    Metodo para todos os produtos em cada categoria.
    Nesse metodo, você tem a criação de um objeto categoria que contem todos os objetos filtrados pelo slug da url
    (identificador unico que é como se fosse um ID)
    """
    #criação do objeto category já filtrado pelo identificador unico.
    category = Category.objects.get(slug=slug)
    
    #criação de um contexto, contendo a categoria atual e a categoria já filtrada contendo todos os produtos. 
    context = {
        'current_category' : category,
        'product_list' : Product.objects.filter(category=category),

    }
    #renderização da pagina com o contexto e o template category.html.
    return render(request, 'catalog/category.html', context)

def product(request, slug):
    """
    Este metodo, é responsavel, para pesquisar apenas uma produto, que é pesquisado também pelo slug da URL.
    """
    #criação do objeto produto, que tem apenas uma posição.
    product = Product.objects.get(slug=slug)
    #criação de um contexto para acessar os atributos no html.
    context = {

        'product' : product

    }
    #renderização do tempalte product.html junto com o contexto. 
    return render(request, 'catalog/product.html', context)
