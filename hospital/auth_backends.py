
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from django.utils import timezone
from .models import User

class CustomAuthBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(username=username)
            
            # Check if account is locked
            if user.is_account_locked():
                return None
                
            if user.check_password(password):
                # Reset failed attempts on successful login
                user.failed_login_attempts = 0
                user.save()
                return user
            else:
                # Increment failed attempts
                user.failed_login_attempts += 1
                if user.failed_login_attempts >= 5:
                    user.lock_account(30)  # Lock for 30 minutes
                user.save()
                return None
                
        except UserModel.DoesNotExist:
            return None

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
