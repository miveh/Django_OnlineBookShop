from django.test import TestCase
from django.urls import reverse
from book.models import Category, Book


class CategoryModelTest(TestCase):
    """
    این کلاس یک تست برای مدل category است.
    """

    def setUp(self):
        Category.objects.create(category='just a test')

    def test_category_name(self):
        category = Category.objects.get(id=1)
        expect_object_name = f'{category.category}'
        self.assertEqual(expect_object_name, 'just a test')


class BookModelTest(TestCase):
    """
    این کلای یک تست برای مدل book است
    """

    def setUp(self):
        Book.objects.create(name='just test', author='test', price=2000, description='just a test')

    def test_book_name(self):
        book = Book.objects.get(id=1)
        expect_object_name = f'{book.name}'
        self.assertEqual(expect_object_name, 'just test')


class HomePageViewTest(TestCase):
    """
    این کلاس یک تست برای ویو home است.
    """

    def setUp(self):
        Category.objects.create(category='another test')

    def test_view_url_exists_at_proper_location(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_by_name(self):
        resp = self.client.get(reverse('home'))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('home'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'home.html')