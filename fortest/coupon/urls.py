from django.urls import path
from coupon.views import coupons, CashCouponCreateView

urlpatterns = [
    path('coupons/', coupons, name='coupons'),
    path('cash/', CashCouponCreateView.as_view(), name='cashcoupons'),
]
