from django.contrib.auth.models import AbstractUser
from django.db import models
from account.managers import CustomUserManager


class CustomUser(AbstractUser):
    """
    این کلاس برای ساخت مدل یوزر است که دو نوع کاربر کارمند و مشتری هم از این ارث می برند.
    """

    class Meta:
        verbose_name = 'مدیر'
        verbose_name_plural = 'مدیران'

    username = None
    device = models.CharField(max_length=200, null=True, blank=True)
    national_code = models.CharField(verbose_name='کدملی', max_length=10, default=0)
    email = models.EmailField(verbose_name='ایمیل', unique=True)
    first_name = models.CharField(verbose_name='نام', max_length=150, blank=True)
    last_name = models.CharField(verbose_name='نام خانوادگی', max_length=150, blank=True)
    is_anonymous_user = models.BooleanField(verbose_name='کاربرناشناس', default=False)
    is_staff = models.BooleanField(
        verbose_name='کارمند',
        default=False,
    )
    is_active = models.BooleanField(
        verbose_name='فعال',
        default=True,

    )
    # password = models.CharField(verbose_name='رمزعبور', max_length=128)
    last_login = models.DateTimeField(verbose_name='آخرین ورود', blank=True, null=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Customer(CustomUser):
    """
    این کلاس برای ایجاد مشتریان است.
    """

    class Meta:
        proxy = True
        verbose_name = 'مشتری'
        verbose_name_plural = 'مشتریان'


class Staff(CustomUser):
    """
    این کلاس برای ایجاد کارمندان است.
    """

    class Meta:
        proxy = True
        verbose_name = 'کارمند'
        verbose_name_plural = 'کارمندان'


class ShippingAddress(models.Model):
    """
    ایجاد یک جدول برای نگهداری تمامی آدرس ها
    """

    class Meta:
        verbose_name = 'آدرس'
        verbose_name_plural = 'آدرس ها'

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='کاربر')
    city = models.CharField(max_length=40, verbose_name='شهر')
    address = models.CharField(max_length=300, verbose_name='محله، خیابان، کوچه...')
    default_address = models.BooleanField(default=False, verbose_name='آدرس اصلی')

    def __str__(self):
        return f'{self.id}'
