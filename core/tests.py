from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.http import HttpRequest
from django.http import HttpResponse
from django.core import mail



#Classe para efetuar os testes d aaplicacao Core.

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
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'index.html')

#testes unitarios para o envio de e-mail
class ContactViewTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('contact')

    def test_view_ok(self):
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact.html')
    #teste para testar um erro no envio de e-mail    
    def test_form_error(self):
        #dados errados para o form
        data = {'name' : '', 'message' : '', 'email' : ''}
        response = self.client.post(self.url, data)
        #verificando abaixo se em todos os campos sao obrigatorios.
        self.assertFormError(response, 'form', 'name', 'Este campo é obrigatório.')
        self.assertFormError(response, 'form', 'email', 'Este campo é obrigatório.')
        self.assertFormError(response, 'form', 'message', 'Este campo é obrigatório.')

    # teste para verificar o sucesso de envio de email    
    def test_form_error_ok(self):
        #dados validos para mandar o e-mail
        data = {'name' : 'test', 'message' : 'test', 'email' : 'test@contato.com'}
        response = self.client.post(self.url, data)
        #verificando se no contexto, tem algo com 'success'
        self.assertTrue(response.context['success'])
        self.assertEquals(len(mail.outbox), 1)
        self.assertEquals(mail.outbox[0].subject, 'Contato do Pye-commerce')






