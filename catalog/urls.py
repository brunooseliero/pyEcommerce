from django.conf.urls import url

from . import views

urlpatterns = [
    #Url base, que vai trazer todos os produtos. 
    url(r'^$', views.product_list,name='product_list'),
    #Url para epsquisar todos os produtos em cada categoria.
    url(r'^(?P<slug>[\w_-]+)/$', views.category,name='category'),
    #Url que vai mostrar somente um produto. 
    url(r'^produto/(?P<slug>[\w_-]+)/$', views.product,name='product'),


]
