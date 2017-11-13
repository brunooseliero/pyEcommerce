# coding=utf-8
import re
from django.db import models
from django.core import validators
from django.contrib.auth.models import AbstractBaseUser, UserManager, PermissionsMixin

class User(AbstractBaseUser, PermissionsMixin):
    
    username = models.CharField(
        'Usuário / E-mail', max_length=30, unique=True, validators=[
            validators.RegexValidator(
                re.compile('^[\w.@+-]+$'),
                'Informe um nome de usuário válido. '
                'Este valor deve conter apenas letras, números '
                'e os caracteres: @/./+/-/_ .', 'invalid'
            )
        ], help_text='Um nome curto que será usado para identificá-lo de forma única na plataforma'
    )
    name = models.CharField('Nome', max_length=100, blank=True)
    email = models.EmailField('E-mail', unique=True)
    street = models.CharField('Rua', max_length=100, blank=False)
    number = models.IntegerField('Número', blank=False)
    complement = models.CharField('Complemento', max_length=100, blank=False)
    district = models.CharField('Bairro', max_length=100, blank=False)
    postal_code = models.CharField('CEP', max_length=8, blank=False)
    city = models.CharField('Cidade', max_length=100, blank=False)
    state = models.CharField('Estado', max_length=2, blank=False)
    country = models.CharField('País', max_length=10, blank=False)
    is_staff = models.BooleanField('Equipe', default=False)
    is_active = models.BooleanField('Ativo', default=True)
    date_joined = models.DateTimeField('Data de Entrada', auto_now_add=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'street', 'number', 'complement', 'district', 'postal_code', 'city', 'state', 'country']

    objects = UserManager()

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
    
    def __str__(self):
        return self.name or self.username

    def get_full_name(self):
        return str(self)

    def get_short_name(self):
        return str(self).split(" ")[0]
