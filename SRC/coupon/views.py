from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView
from coupon.forms import CartCouponForm, BookCashCouponForm, BookPercentCouponForm


class CartCouponCreationView(LoginRequiredMixin, CreateView):
    """
    ایجاد تخفیف
    """

    form_class = CartCouponForm
    template_name = 'coupon/coupon_form.html'
    success_url = reverse_lazy('staff')


class BookCashCouponCreationView(LoginRequiredMixin, CreateView):
    """
    ایجاد تخفیف
    """

    form_class = BookCashCouponForm
    template_name = 'coupon/coupon_form.html'
    success_url = reverse_lazy('staff')


class BookPercentCouponCreationView(LoginRequiredMixin, CreateView):
    """
    ایجاد تخفیف
    """

    form_class = BookPercentCouponForm
    template_name = 'coupon/coupon_form.html'
    success_url = reverse_lazy('staff')