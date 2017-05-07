#coding=utf-8
from django.shortcuts import render
from django.views.generic import CreateView
from .forms import UserAdminCreationForm
from django .core.urlresolvers import reverse_lazy

from .models import User

class RegisterView(CreateView):

    model = User
    template_name = 'accounts/register.html'
    form_class = UserAdminCreationForm
    success_url = reverse_lazy('index')

register = RegisterView.as_view()



