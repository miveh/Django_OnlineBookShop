from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.generic import CreateView

from coupon.models import CartCoupon


def coupons(request):
    return render(request, 'coupon/coupons.html')


class CashCouponCreateView(CreateView):
    model = CartCoupon
    template_name = 'coupon/cash_coupon_new.html'
    fields = ['code', 'discount']
