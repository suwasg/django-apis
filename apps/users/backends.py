# from django.contrib.auth.backends import ModelBackend
# from django.contrib.auth import get_user_model

# UserModel = get_user_model()

# class EmailBackend(ModelBackend):
#     def authenticate(self, request, email=None, password=None, **kwargs):
#         try:
#             user = UserModel.objects.get(email=email)
#         except UserModel.DoesNotExist:
#             return None
#         if user.check_password(password) and self.user_can_authenticate(user):
#             return user
#         return None

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

class EmailBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        UserModel = get_user_model()
        if email is None or password is None:
            return None
        try:
            user = UserModel.objects.get(Q(email__iexact=email))
        except UserModel.DoesNotExist:
            return None
        except UserModel.MultipleObjectsReturned:
            return None
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
