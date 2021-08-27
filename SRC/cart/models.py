from django.db import models
from django.urls import reverse


class Cart(models.Model):
    """
    سبد خرید
    """

    class Meta:
        ordering = ('id',)
        verbose_name = 'سبد خرید'
        verbose_name_plural = 'سبدهای خرید'

    user = models.ForeignKey('account.CustomUser', on_delete=models.CASCADE, verbose_name='کاربر')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.id}'

    def get_absolute_url(self):
        return reverse('cart', kwargs={id: self.id})


class CartItems(models.Model):
    """
    یک سفارش شامل یک عنوان کتاب با هر تعداد دلخواه و فقط در یک سبد خرید
    """

    ORDER_STATUS = [
        ('F', 'finalized'),
        ('U', 'unordered'),
        ('O', 'ordering'),
    ]

    class Meta:
        verbose_name = 'سفارش'
        verbose_name_plural = 'سفارشات'

    book = models.ForeignKey('book.Book', on_delete=models.CASCADE)
    ordered = models.CharField(max_length=4, choices=ORDER_STATUS, default='U')
    quantity = models.PositiveSmallIntegerField(default=1)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)

    @property
    def total_price(self):
        """
        :return: قیمت کل یک سفارش برابر با قیمت کتاب بعد از تخفیف ضرب در تعداد انتخاب شده.
        """

        return self.book.total_price * self.quantity

    def __str__(self):
        return f'{self.id}'

    def get_absolute_url(self):
        return reverse('cart_item_detail', kwargs={id: self.id})


class FinalizedOrders(models.Model):
    """
    یک فاکتور خرید شامل تعدادی از سفارش ها ی یک سبد خرید و یک آدرس از کاربر برای انتقال به درگاه پرداخت
    """

    class Meta:
        verbose_name = 'فاکتورخرید'
        verbose_name_plural = 'فاکتورهای خرید'

    shipping_address = models.ForeignKey('account.ShippingAddress', on_delete=models.CASCADE)
    discount = models.IntegerField(default='0')
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    item = models.ManyToManyField(CartItems)
    price = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now=True)
    payment = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.id}'

    @property
    def factor_total_price(self):
        """
        :return: قیمت کل یک فاکتور برابر: قیمت کل منهای تخفیف اعمال شده روی سبد خرید
        """

        total_price = (self.price * (100 - int(self.discount))) / 100
        return total_price
