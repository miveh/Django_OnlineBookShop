from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView
from coupon.forms import CartCouponForm, BookCashCouponForm, BookPercentCouponForm


class CartCouponCreationView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """
    ایجاد تخفیف
    """

    form_class = CartCouponForm
    template_name = 'coupon/coupon_form.html'
    success_url = reverse_lazy('staff')
    permission_required = 'coupon.add_cartcoupon'


class BookCashCouponCreationView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """
    ایجاد تخفیف
    """

    form_class = BookCashCouponForm
    template_name = 'coupon/coupon_form.html'
    success_url = reverse_lazy('staff')
    permission_required = 'coupon.add_bookcashcoupon'


class BookPercentCouponCreationView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """
    ایجاد تخفیف
    """

    form_class = BookPercentCouponForm
    template_name = 'coupon/coupon_form.html'
    success_url = reverse_lazy('staff')
    permission_required = 'coupon.add_bookpercentcoupon'
