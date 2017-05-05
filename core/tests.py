from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.core import mail
from django.contrib.auth import get_user_model
from django.conf import settings

from model_mommy import mommy
 
User = get_user_model()


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

class LoginViewTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.login_url = reverse('login')
        self.user = mommy.prepare(settings.AUTH_USER_MODEL)
        self.user.set_password('123')
        self.user.save()
    
    def tearDown(self):
        self.user.delete()

    def test_login_ok(self):
        response = self.client.get(self.login_url)
        self.assertAlmostEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
        data = {'username': self.user.username, 'password' : '123'}
        response = self.client.post(self.login_url, data)
        redirect_url = reverse(settings.LOGIN_REDIRECT_URL)
        self.assertRedirects(response, redirect_url, status_code=302)
        self.assertTrue(response.wsgi_request.user.is_authenticated())

    def test_user_error(self):
        data = {'username': self.user.username, 'password' : '1234'}
        response = self.client.post(self.login_url, data)
        self.assertAlmostEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
        error_msg = ('Por favor, entre com um usuário  e senha corretos. Note que '
        'ambos os campos diferenciam maiúsculas e minúsculas.')
        self.assertFormError(response, 'form', None, error_msg)

class RegisterViewTestCase(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register')

    def test_register_ok(self):
        data = {'username': 'gileno', 'password1': 'teste123', 'password2': 'teste123'}
        response = self.client.post(self.register_url, data)
        index_url = reverse('index')
        self.assertRedirects(response, index_url)
        self.assertEquals(User.objects.count(), 1)






