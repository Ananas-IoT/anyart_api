from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class EmailAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        user = UserModel.objects.get(email=username)
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
