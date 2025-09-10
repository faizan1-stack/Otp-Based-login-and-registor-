from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class AuthBackend(ModelBackend):
    def authenticate(self, request, username=None, email= None , password = None , **kwargs):
        User = get_user_model()
        email_to_check = email or username
        try:
            user = User.objects.get(email=email_to_check)
            if user.check_password(password) and self.authenticate(user):
                return user
        except User.DoesNotExist:
            return None
        return None

