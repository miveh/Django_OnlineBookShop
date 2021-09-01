from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from account.models import ShippingAddress


class AddressFormTest(TestCase):
    """
    این یک تست برای تست آدرس ها است.
    """

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='test@email.com',
            password='secret',
            national_code=123456789,
        )

        self.address = ShippingAddress.objects.create(
            city='A good city',
            address='Nice address',
            user=self.user,
        )

    def test_string_representation(self):
        address = ShippingAddress(city='A sample city')
        self.assertEqual(str(address.city), address.city)

    def test_address_create_view(self):
        response = self.client.post(reverse('address'), {
            'city': 'A good city',
            'address': 'Nice address',
            'user': self.user.id,
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(ShippingAddress.objects.last().city, 'A good city')
        self.assertEqual(ShippingAddress.objects.last().address, 'Nice address')


class SignupPageTests(TestCase):
    """
    این یک تست برای ثبت نام کاربر است.
    """

    email = 'newuser@email.com'
    password = 'secret'

    def test_signup_page_status_code(self):
        response = self.client.get('/accounts/signup/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_by_name(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/signup.html')

    def test_signup_form(self):
        new_user = get_user_model().objects.create_user(self.email, self.password)
        self.assertEqual(get_user_model().objects.all().count(), 1)
        self.assertEqual(get_user_model().objects.all()[0].email, self.email)
