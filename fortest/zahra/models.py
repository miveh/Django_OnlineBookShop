from django.db import models


# Create your models here.
class Ca(models.Model):
    name = models.CharField(max_length=40)


class Cart(models.Model):
    name = models.CharField(max_length=40)


class Ro(models.Model):
    name = models.CharField(max_length=40)


class To(models.Model):
    name = models.CharField(max_length=40)
    ca = models.ForeignKey(Ca, on_delete=models.CASCADE)
    ro = models.ForeignKey(Ro, on_delete=models.CASCADE)
    cart = models.ManyToManyField(Cart)

