# coding=utf-8

from django import forms
from django.conf import settings
from django.core.mail import send_mail


class ContactForm(forms.Form):
    """
    Criação de formulários no Django.

    o Django tem um sistema de formulários bem diferente do que eu estou acostumado, você vai setar
    os tipos de campos direto no código, e colocar os parâmetros.
    Nada mais e do que uma classe onde os atributos sao os campos dos formulários,
    e a classe tem que herdar de forms.Form que e a classe relacionada ao
    sistema de formulários do Django.
    """

    name = forms.CharField(label='Nome')
    email = forms.EmailField(label='E-mail')
    message = forms.CharField(label='Mensagem', widget=forms.Textarea())

    # def __init__(self, *args, **kwargs):
    #super(ContactForm, self).__init__(*args, **kwargs)
    #self.fields['name'].widget.attrs['class'] = 'form-control'
    #self.fields['email'].widget.attrs['class'] = 'form-control'
    #self.fields['message'].widget.attrs['class'] = 'form-control'
    def send_mail(self):
        # recuperando os valores que foram digitados no form
        # e transformando os mesmos em objetos python com o metodo
        # clened_data.
        name = self.cleaned_data['name']
        email = self.cleaned_data['email']
        message = self.cleaned_data['message']
        # compondo a mensagem com nome, email e a mensagem em si.
        message = 'Nome: {0}\nEmail:{1}\n{2}'.format(name, email, message)
        # metodo que recebe:
        # 1 parametro o assunto do email;
        # 2 parametro a mensagem que vai ser enviada;
        # 3 de quem a mensagem sera enviada;
        # 4 para quem a mensagem sera enviada.
        send_mail('Contato do Pye-commerce', message, settings.DEFAULT_FROM_EMAIL,
                  [settings.DEFAULT_FROM_EMAIL])
