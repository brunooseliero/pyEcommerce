#coding=utf-8
"""
Esse arquivo esta sendo criado, para carregar todas as categorias de produtos em todas as paginas. 

O django tem um mecanismo que, quando colocado no dicionario de templates, ele executa esses arquivos antes de 
renderizar qualquer template, eliminando o problema de ter que colocar em todos os metodos da view.py.

"""
from .models import Category

def categories(request):
    return {
        'categories' : Category.objects.all()

    }

