#coding=utf-8
from django.shortcuts import render
from django.views.generic import CreateView, TemplateView, UpdateView, FormView
from .forms import UserAdminCreationForm
from django .core.urlresolvers import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import PasswordChangeForm


from .models import User

class RegisterView(CreateView):
    
    # mdelo a ser usada
    model = User
    # template .html a ser usado
    template_name = 'accounts/register.html'
    # tipo qual form vai ser usado
    form_class = UserAdminCreationForm
    # url de sucesso, se o registro der certo
    success_url = reverse_lazy('index')


class IndexView(LoginRequiredMixin, TemplateView):
    
    # renderização da pagina index na aplicação de contas
    template_name = 'accounts/index.html'

class UpdateUserView(LoginRequiredMixin,UpdateView):
    
    # modelo a ser usada
    model = User
    # tempalte .html a ser usado
    template_name = 'accounts/update_user.html'
    # definição de campos que podem ser editados
    fields = ['name', 'email', 'street', 'number', 'complement', 'district', 'postal_code', 'city', 'state', 'country']
    # url de sucesso, se o registro der certo
    success_url = reverse_lazy('accounts:index')

    def get_object(self):
        
        # metodo para retornar o usuário
        return self.request.user

class UpdatePasswordView(LoginRequiredMixin, FormView):
    """
     Metodo para alteração de senha.
    """
    # template que vai ser usado
    template_name = 'accounts/update_password.html'
    # url de sucesso, se o registro der certo
    success_url = reverse_lazy('accounts:index')
    # tipo de formulário
    form_class = PasswordChangeForm

    def get_form_kwargs(self):
        kwargs = super(UpdatePasswordView, self).get_form_kwargs()
        kwargs['user'] = self.request.user

        return kwargs

    def form_valid(self, form):
        form.save()
        return super(UpdatePasswordView, self).form_valid(form)



index = IndexView.as_view()
register = RegisterView.as_view()
update_user = UpdateUserView.as_view()
update_password = UpdatePasswordView.as_view()



