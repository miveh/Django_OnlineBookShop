from django.db import models

# Create your models here.
from Book_Store import settings
from accounts.models import MyUser
from book.models import Book


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    STATUS_CHOICES = [('D', 'delete'), ('W', 'waiting'), ('O', 'ordered')]
    order_status = models.IntegerField(max_length=1, choices=STATUS_CHOICES)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    discount = models.IntegerField(blank=True, null=True, default=None)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'{self.user} - {str(self.id)}'

    def get_total_price(self):
        pass


class CartItems(models.Model):
    order = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Book, on_delete=models.CASCADE)
    # price = models.IntegerField()
    quantity = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    def total(self):
        return self.quantity * self.product.price

    def name(self):
        return self.product.title
