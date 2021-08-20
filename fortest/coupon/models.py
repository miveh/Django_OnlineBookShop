from django.db import models


# Create your models here.
class CartCoupon(models.Model):
    """
    This discount only applies to books.
    """
    class Meta:
        verbose_name = 'تخفیف'
        verbose_name_plural = 'تخفیف درصدی سبدخرید'

    code = models.CharField(max_length=30)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    is_active = models.BooleanField(default=False)
    discount_percent = models.IntegerField(default=0)

    def __str__(self):
        return self.code


