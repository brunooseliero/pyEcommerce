#coding=utf-8
from django.shortcuts import render
from django.views.generic import CreateView, TemplateView, UpdateView
from .forms import UserAdminCreationForm
from django .core.urlresolvers import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin


from .models import User

class RegisterView(CreateView):

    model = User
    template_name = 'accounts/register.html'
    form_class = UserAdminCreationForm
    success_url = reverse_lazy('index')


class IndexView(LoginRequiredMixin, TemplateView):

    template_name = 'accounts/index.html'

class UpdateUserView(LoginRequiredMixin,UpdateView):

    model = User
    template_name = 'accounts/update_user.html'
    fields = ['name', 'email']
    success_url = reverse_lazy('accounts:index')

    def get_object(self):

        return self.request.user




index = IndexView.as_view()
register = RegisterView.as_view()
update_user = UpdateUserView.as_view()



