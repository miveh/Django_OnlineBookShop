from django.db import models


class CartCoupon(models.Model):
    """
    کد تخفیف برای سبد خرید
    """

    class Meta:
        verbose_name = 'تخفیف درصدی سبد'
        verbose_name_plural = 'تخفیف درصدی سبدهای خرید'

    code = models.CharField(verbose_name='کد', max_length=30)
    valid_from = models.DateTimeField(verbose_name='تاریخ شروع')
    valid_to = models.DateTimeField(verbose_name='تاریخ انقضا')
    is_active = models.BooleanField(verbose_name='فعال', default=False)
    discount_percent = models.IntegerField(verbose_name='درصد تخفیف', default=0)

    def __str__(self):
        return self.code


class BookCashCoupon(models.Model):
    """
    تخفیف نقدی کتاب. هر تخفیف می تواند روی چندین کتاب اعمال شود و هر کتاب می تواند چندین کد تخفیف داشته باشد.
    """

    class Meta:
        verbose_name = 'تخفیف نقدی کتاب'
        verbose_name_plural = 'تخفیف نقدی کتاب ها'

    valid_from = models.DateTimeField(verbose_name='تاریخ شروع')
    valid_to = models.DateTimeField(verbose_name='تاریخ انقضا')
    is_active = models.BooleanField(verbose_name='فعال', default=False)
    discount_price = models.IntegerField(verbose_name='مبلغ تخفیف', default=0)
    books = models.ManyToManyField('book.Book', verbose_name='کتاب ها',  blank=True)

    def __str__(self):
        return f'{self.discount_price}'


class BookPercentCoupon(models.Model):
    """
    تخفیف درصدی کتاب. هر تخفیف می تواند روی چندین کتاب اعمال شود و هر کتاب می تواند چندین کد تخفیف داشته باشد.
    """

    class Meta:
        verbose_name = 'تخفیف درصدی کتاب'
        verbose_name_plural = 'تخفیف درصدی کتاب ها'

    valid_from = models.DateTimeField(verbose_name='تاریخ شروع')
    valid_to = models.DateTimeField(verbose_name='تاریخ انقضا')
    is_active = models.BooleanField(verbose_name='فعال', default=False)
    discount_percent = models.IntegerField(verbose_name='درصد تخفیف', default=0)
    books = models.ManyToManyField('book.Book', verbose_name='کتاب ها', blank=True)

    def __str__(self):
        return f'{self.discount_percent}'
