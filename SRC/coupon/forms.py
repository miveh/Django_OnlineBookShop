from django import forms
from coupon.models import CartCoupon, BookCashCoupon, BookPercentCoupon


class CartCouponForm(forms.ModelForm):
    """
    فرم ایجاد کوپن سبد خرید
    """

    class Meta:
        model = CartCoupon
        fields = '__all__'


class BookCashCouponForm(forms.ModelForm):
    """
    فرم ایجاد کوپن کتاب
    """

    class Meta:
        model = BookCashCoupon
        fields = '__all__'


class BookPercentCouponForm(forms.ModelForm):
    """
    فرم ایجاد کوپن کتاب
    """

    class Meta:
        model = BookPercentCoupon
        fields = '__all__'
