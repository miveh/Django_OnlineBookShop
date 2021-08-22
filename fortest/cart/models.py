from django.db import models
from django.urls import reverse

from accounts.models import ShippingAddress


class Cart(models.Model):
    class Meta:
        ordering = ('id',)
        verbose_name = 'سبد خرید'
        verbose_name_plural = 'سبدهای خرید'

    # user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # finalized_orders = models.ForeignKey(FinalizedOrders, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f'{self.id}'

    def get_absolute_url(self):
        return reverse('cart', kwargs={id: self.id})

    # def get_total_price_cart(self):
    #     # total = sum(item.get_cost() for item in self.items.all())
    #     total = sum(item.total_price for item in CartItems.objects.filter(cart__id=2))
    #     return total


class CartItems(models.Model):
    ORDER_STATUS = [
        ('F', 'finalized'),
        ('U', 'unordered'),
        ('O', 'ordering'),
    ]

    class Meta:
        verbose_name = 'سفارش'
        verbose_name_plural = 'سفارشات'

    # user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    book = models.ForeignKey('book.Book', on_delete=models.CASCADE)
    ordered = models.CharField(max_length=4, choices=ORDER_STATUS, default='U')
    quantity = models.PositiveSmallIntegerField(default=1)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, blank=True, null=True)

    @property
    def total_price(self):
        return self.book.total_price * self.quantity

    def __str__(self):
        return f'{self.book} {self.quantity} عدد در سبد {self.cart.id} با وضعیت سفارش : {self.ordered}'

    def get_absolute_url(self):
        return reverse('cartitemdetail', kwargs={id: self.id})


class FinalizedOrders(models.Model):
    class Meta:
        verbose_name = 'فاکتورخرید'
        verbose_name_plural = 'فاکتورهای خرید'

    shipping_address = models.ForeignKey(ShippingAddress, on_delete=models.CASCADE, blank=True, null=True)
    discount = models.IntegerField(default='0')
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, blank=True, null=True)
    item = models.ManyToManyField(CartItems)
    price = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now=True)
    payment = models.BooleanField(default=False)

    def __str__(self):
        return f'تعداد {self.item.count()} محصول از سبد شماره ی {self.cart.id} در فاکتور شماره {self.id}' \
               f' برای ارسال به {self.shipping_address.city}،{self.shipping_address.address} با وضعیت {self.payment} ثبت شد.'

    @property
    def factor_total_price(self):
        total_price = (self.price * (100 - int(self.discount))) / 100

        return total_price
