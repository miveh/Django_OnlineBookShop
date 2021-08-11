from django.db import models


# Create your models here.
class Category(models.Model):
    class Meta:
        verbose_name_plural = 'categories'

    name = models.CharField(max_length=40, unique=True)
    slug = models.CharField()


class Book(models.Model):
    title = models.CharField(max_length=200, unique=True)
    author = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    stock = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=1000)
    slug = models.SlugField()
    category = models.ManyToManyField(Category, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.title
