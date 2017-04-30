#coding=utf-8
"""
Criando as classes Modelo, para a aplicacao funcionar.

Primeiro eu crio a classe categoria(Category) que com as anotacoes do Django,
vao criar as tabelas no banco pra mim.

Depois eu crio a tabela prdutos, que tem uma chave estrangeira de categoria para identificar a
qual categoria aquele produto pertence.

"""
from django.db import models
from django.core.urlresolvers import reverse

class Category(models.Model):
    #criando os atributos das classes e definindo as notacoes para o banco de dados.
    name = models.CharField('Nome', max_length=100)
    slug = models.SlugField('Identificador', max_length=100)
    #campo para identificar quando a categoria foi criada.
    created = models.DateTimeField('Criado em', auto_now_add=True)
    #campo para saber quando teve a ultima modificacao.
    modified = models.DateTimeField('Modificado em', auto_now_add=True)

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['name']

    def __str__(self):
        return str(self.name)
    
    def get_absolute_url(self):
        return reverse('catalog:category', kwargs={'slug': self.slug})

class Product(models.Model):

    name = models.CharField('Nome', max_length=100)
    slug = models.SlugField('Identificador', max_length=100)
    #atributo da classe categoria e chave estrangeira para o banco.
    category = models.ForeignKey('catalog.Category', verbose_name='Categoria')
    description = models.TextField('Descrição', blank=True)
    price = models.DecimalField('Preço', decimal_places=2, max_digits=10)
    created = models.DateTimeField('Criado em', auto_now_add=True)
    modified = models.DateTimeField('Modificado em', auto_now_add=True)

    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'
        ordering = ['name']

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse('catalog:product', kwargs={'slug': self.slug})



