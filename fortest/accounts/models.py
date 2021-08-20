from django.db import models

from fortest import settings


class ShippingAddress(models.Model):
    class Meta:
        verbose_name = 'آدرس'
        verbose_name_plural = 'آدرس ها'

    # user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    user = models.IntegerField(default=2)
    city = models.CharField(max_length=40)
    address = models.CharField(max_length=300)
    default_address = models.BooleanField(default=False)

    def __str__(self):
        return f'مشتری شماره {self.user} با آدرس : {self.city} ، {self.address}'
