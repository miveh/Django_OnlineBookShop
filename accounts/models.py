from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
from accounts.managers import UserManager


class CustomUser(AbstractUser):
    """
    is a superuser or staff or customer? بیشتر فاز 3 روی این قسمت کار می کنم
    """
    email = models.EmailField(max_length=100, unique=True)
    full_name = models.CharField(max_length=100)
    admin = models.BooleanField(default=False)
    staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    objects = UserManager()  # باید اضافه کنمش
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']  # موقع ساخت سوپریوزر ازم فول نیم هم میخواد.

    def __str__(self):
        return self.email

    # این پراپرتی مشخض می کنه این یوزر کارمنده یا نه.
    @property
    def is_staff(self):
        if self.is_admin:
            return True
        return self.staff

    # این پراپرتی مشخض می کنه این یوزر ادمین یا نه.
    @property
    def is_admin(self):
        return self.admin
