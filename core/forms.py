#coding=utf-8

from django import forms

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

    #def __init__(self, *args, **kwargs):
        #super(ContactForm, self).__init__(*args, **kwargs)
        #self.fields['name'].widget.attrs['class'] = 'form-control'
        #self.fields['email'].widget.attrs['class'] = 'form-control'
        #self.fields['message'].widget.attrs['class'] = 'form-control'
