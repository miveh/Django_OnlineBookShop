import datetime
from django.utils import timezone

from django.contrib.auth import get_user_model
from django.test import TestCase
from coupon.models import CartCoupon, BookCashCoupon, BookPercentCoupon


class CartCouponTest(TestCase):
    """
    این یک تست برای مدل کوپن تخفیف سبد خرید است.
    """

    def setUp(self):
        self.cart_coupon = CartCoupon.objects.create(
            valid_to=(timezone.datetime(2021, 2, 1)),
            valid_from=(timezone.datetime(2021, 11, 1)),
            discount_percent=10
        )

    def test_coupon_content(self):
        self.assertEqual(f'{self.cart_coupon.valid_to}', str(timezone.datetime(2021, 2, 1)))
        self.assertEqual(f'{self.cart_coupon.valid_from}', str(timezone.datetime(2021, 11, 1)))
        self.assertEqual(f'{self.cart_coupon.discount_percent}', str(10))


class BookCashCouponTest(TestCase):
    """
    این یک تست برای مدل کوپن نقدی کتاب است.
    """

    def setUp(self):
        self.cache_book_coupon = BookCashCoupon.objects.create(
            valid_to=(datetime.datetime(2021, 2, 1)),
            valid_from=(datetime.datetime(2021, 9, 10)),
            discount_price=10
        )

    def test_coupon_content(self):
        self.assertEqual(f'{self.cache_book_coupon.valid_to}', str(datetime.datetime(2021, 2, 1)))
        self.assertEqual(f'{self.cache_book_coupon.valid_from}', str(datetime.datetime(2021, 9, 10)))
        self.assertEqual(f'{self.cache_book_coupon.discount_price}', str(10))


class BookPercentCouponTest(TestCase):
    """
    این یک تست برای مدل کوپن درصدی کتاب است.
    """

    def setUp(self):
        self.percent_book_coupon = BookPercentCoupon.objects.create(
            valid_to=(datetime.datetime(2021, 2, 1)),
            valid_from=(datetime.datetime(2021, 7, 1)),
            discount_percent=10
        )

    def test_coupon_content(self):
        self.assertEqual(f'{self.percent_book_coupon.valid_to}', str(datetime.datetime(2021, 2, 1)))
        self.assertEqual(f'{self.percent_book_coupon.valid_from}', str(datetime.datetime(2021, 7, 1)))
        self.assertEqual(f'{self.percent_book_coupon.discount_percent}', str(10))
