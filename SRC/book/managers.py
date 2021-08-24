from django.db import models
from book.models import Category


class CategoryManager(models.Manager):

    def get_not_null_category(self):
        """
        :return: تمامی دسته بندی هایی که شامل کتاب هستند.
        """
        null_category = Category.objects.exclude(book__isnull=True)
        return null_category
