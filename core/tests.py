from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.http import HttpRequest
from django.http import HttpResponse

"""
Classe para efetuar os testes d aaplicacao Core.
"""
class IndexViewTestCase(TestCase):

    #Metodo de setUp, para evitar duplicacao de codigo;
    def setUp(self):
        self.client = Client()
        self.url = reverse('index')
    #metodo para excluir coisas dos metodos dods testes
    def tearDown(self):
        pass
     #metodo para confirmar o template usado no index.html
    def test_template_used(self):
        response = self.client.get(self, url)
        self.assertTemplateUsed(response, 'index.html')

