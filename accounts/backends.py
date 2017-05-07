#coding=utf-8   

from django.contrib.auth.backends import ModelBackend as BaseBackend 

from .models import User

class ModelBackend(BaseBackend):

    def authenticate(self, username=None, password=None):

        if not username is None:
            UserModel = User()
            try:
                user = User.objects.get(email=username)
                if user.check_password(password):
                    return user
            except User.DoesNotExist:
                pass
