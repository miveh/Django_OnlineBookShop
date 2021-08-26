from django.urls import path
from coupon.views import CartCouponCreationView, BookCashCouponCreationView, BookPercentCouponCreationView

#

urlpatterns = [
    path('cart_coupon/', CartCouponCreationView.as_view(), name='staff_add_cart_coupon'),
    path('book_cache_coupon/', BookCashCouponCreationView.as_view(), name='staff_add_book_cache_coupon'),
    path('book_percent_coupon/', BookPercentCouponCreationView.as_view(), name='staff_add_book_percent_coupon'),
]
