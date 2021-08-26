from django import forms
from book.models import Book, Category


class BookCreationForm(forms.ModelForm):
    """
    فرم ایجاد کتاب
    """

    class Meta:
        model = Book
        fields = ['name', 'author', 'price', 'stock', 'description', 'category', 'image']
        # fields = '__all__'

    description = forms.CharField(max_length=500, widget=forms.Textarea())
    use_required_attribute = ['name', 'author', 'price', 'stock', 'category', 'image']


class CategoryCreationForm(forms.ModelForm):
    """
    فرم ایجاد دسته بندی
    """

    class Meta:
        model = Category
        fields = ['category']

    use_required_attribute = ['category']