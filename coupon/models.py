from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


# Create your models here.
class CashCoupon(models.Model):
    code = models.CharField(max_length=30, unique=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    discount = models.BigIntegerField()
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.code


class PercentCoupon(models.Model):
    code = models.CharField(max_length=30, unique=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    discount = models.IntegerField(max_length=2)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.code


class PercentCouponForCart(models.Model):
    code = models.CharField(max_length=30, unique=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    discount = models.IntegerField(max_length=2)
    active = models.BooleanField(default=False)