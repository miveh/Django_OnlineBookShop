from django.db import models


# Create your models here.
class CartCoupon(models.Model):
    """
    This discount only applies to carts
    """

    class Meta:
        verbose_name = 'تخفیف درصدی سبد'
        verbose_name_plural = 'تخفیف درصدی سبدهای خریده'

    code = models.CharField(max_length=30)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    is_active = models.BooleanField(default=False)
    discount_percent = models.IntegerField(default=0)

    def __str__(self):
        return self.code


class BookCashCoupon(models.Model):
    """
    This discount only applies to books.
    """

    class Meta:
        verbose_name = 'تخفیف نقدی کتاب'
        verbose_name_plural = 'تخفیف نقدی کتاب ها'

    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    is_active = models.BooleanField(default=False)
    discount_price = models.IntegerField(default=0)
    books = models.ManyToManyField('book.Book', blank=True)

    def __str__(self):
        return f'{self.discount_price}'


class BookPercentCoupon(models.Model):
    """
    This discount only applies to books.
    """

    class Meta:
        verbose_name = 'تخفیف درصدی کتاب'
        verbose_name_plural = 'تخفیف درصدی کتاب ها'

    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    is_active = models.BooleanField(default=False)
    discount_percent = models.IntegerField(default=0)
    books = models.ManyToManyField('book.Book', blank=True)

    def __str__(self):
        return f'{self.discount_percent}'
