from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from book.models import Book


class BookCreationForm(forms.ModelForm):
    """
    فرم ایجاد کتاب
    """

    class Meta:
        model = Book
        # fields = ['name', 'author', 'price', 'stock', 'description', 'category', 'image']
        # fields = '__all__'
    # description = forms.CharField(max_length=40, widget=forms.Textarea())
    # use_required_attribute = ['name', 'author', 'price', 'stock', 'category', 'image']
