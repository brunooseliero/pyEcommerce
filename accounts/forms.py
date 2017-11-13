from django.contrib.auth.forms import UserCreationForm
from django import forms

from .models import User

class UserAdminCreationForm(UserCreationForm):

    class Meta:

        model = User
        fields = ['username', 'email', 'street', 'number', 'complement', 'district', 'postal_code', 'city', 'state', 'country']

class UserAdminForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'name', 'is_active', 'is_staff']