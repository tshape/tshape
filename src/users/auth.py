from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


# do i need this?
class UserAuth(ModelBackend):

    def authenticate(self, email=None, password=None):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=email)
        except UserModel.DoesNotExist:
            return None
        if user.check_password(password):
            return user

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
