from django.db import models


# Create your models here.
class Customer(models.Model):
    full_name = models.CharField(max_length=80)
    default_address = models.CharField(max_length=70, blank=True, null=True)
    city = models.CharField(max_length=40, blank=True, null=True)
    postal_code = models.CharField(max_length=10, blank=True, null=True)
    phone = models.CharField(max_length=24, blank=True, null=True)
    email = models.EmailField()
    support_rep_id = models.IntegerField()
    # is_active = models.BooleanField(default=True)
