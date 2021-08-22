from django.contrib import admin

# Register your models here.
from coupon.models import CartCoupon, BookCashCoupon, BookPercentCoupon

admin.site.register(CartCoupon)
admin.site.register(BookCashCoupon)
admin.site.register(BookPercentCoupon)