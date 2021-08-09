from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):

    def create_user(self, email, full_name, password):
        pass

    def create_superuser(self, email, full_name, password):
        pass
