from django.contrib.auth.models import AbstractUser
from django.db import models
# src/users/model.py
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _





# Create your models here.
from accounts.managers import MyUserManager


class MyUser(AbstractUser):
    username = None
    full_name = models.CharField(max_length=50, unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    email = models.EmailField(max_length=100, unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = MyUserManager()
