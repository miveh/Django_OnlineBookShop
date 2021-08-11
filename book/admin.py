from django.contrib import admin

# Register your models here.
from book.models import Book

admin.site.register(Book)