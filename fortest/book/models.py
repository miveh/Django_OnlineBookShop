import random

from django.db import models

# Create your models here.
from django.urls import reverse
from slugify import slugify


class CategoryManager(models.Manager):
    def get_not_null_category(self):
        null_category = Category.objects.exclude(book__isnull=True)
        return null_category


class Category(models.Model):
    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'

    category = models.CharField(max_length=40, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    objects = CategoryManager()

    def save(self, *args, **kwargs):
        to_slug = self.slug
        if to_slug == "":
            to_slug = slugify(str(self.category) + " " + "category")
            qs = Category.objects.filter(slug=to_slug).exists()
            while qs:
                to_slug = slugify(to_slug + " " + str(random.randint(1, 500)))
                qs = Category.objects.filter(slug=to_slug).exists()
        self.slug = to_slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.category

    def get_absolute_url(self):
        return reverse('categorydetail', kwargs={'slug': self.slug})


class Book(models.Model):
    class Meta:
        ordering = ('-price',)
        verbose_name = 'کتاب'
        verbose_name_plural = 'کتاب ها'

    name = models.CharField(max_length=50, unique=True)
    image = models.ImageField(default='product.png', upload_to='books/')
    author = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)
    stock = models.IntegerField(default=1)
    description = models.CharField(max_length=500, default='بدون توضیحات')
    discount = models.ManyToManyField('coupon.CartCoupon', blank=True)
    category = models.ManyToManyField(Category)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        book_slug = self.slug
        if book_slug == "":
            book_slug = slugify(str(self.name) + " " + "book")
            qs = Category.objects.filter(slug=book_slug).exists()
            while qs:
                book_slug = slugify(book_slug + " " + str(random.randint(1, 500)))
                qs = Category.objects.filter(slug=book_slug).exists()
        self.slug = book_slug
        super().save(*args, **kwargs)

    def __str__(self):
        return f'کتاب {self.name} با موجودی {self.stock} عدد'

    def get_absolute_url(self):
        return reverse('bookdetail', kwargs={'slug': self.slug})

    def get_add_to_cart_url(self):
        return reverse('addcart', kwargs={'slug': self.slug})