from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from book.forms import BookCreationForm, CategoryCreationForm
from book.models import Category, Book


class AllBooksView(ListView):
    """
    نمایش تمام کتاب ها در یک صفحه
    """

    model = Book
    template_name = 'book/all_books.html'
    context_object_name = 'books'


class CategoryBooksPageView(DetailView):
    """
    نمایش کتاب های یک دسته بندی
    """
    model = Category
    template_name = 'book/category_books.html'


class BookDetailView(DetailView):
    """
    نمایش جزئیات هر کتاب
    """

    model = Book
    template_name = 'book/book_details.html'


class BookCreationView(LoginRequiredMixin, CreateView):
    """
    ایجاد کتاب
    """

    form_class = BookCreationForm
    template_name = 'book/book_form.html'
    success_url = reverse_lazy('staff')


class CategoryCreationView(LoginRequiredMixin, CreateView):
    """
    ایجاد دسته بندی
    """

    form_class = CategoryCreationForm
    template_name = 'book/category_form.html'
    success_url = reverse_lazy('staff')


class StoreroomView(LoginRequiredMixin, ListView):
    """
    انبار
    """

    model = Book
    context_object_name = 'book_storeroom'
    template_name = 'staff/storeroom.html'


class BookEditView(UpdateView):
    """
    ویرایش کتاب
    """

    model = Book
    template_name = 'book/book_edit.html'
    fields = ['name', 'author', 'price', 'category', 'stock', 'description', 'image']
    success_url = reverse_lazy('storeroom')


class BookDeleteView(DeleteView):
    """
    حذف کتاب
    """

    model = Book
    template_name = 'book/book_delete.html'
    success_url = reverse_lazy('storeroom')


def search_bar(request):
    """
    :param request: اسم یک کتاب یا یک نویسنده یا بخشی از آنها
    :return: لیستی از کناب هایی که نام یا نویسنده ی ان سرچ شده
    """

    if request.method == 'POST':
        searched = request.POST['searched']
        book_by_name = Book.objects.filter(name__contains=searched)
        book_by_author = Book.objects.filter(author__contains=searched)
        return render(request, 'book/search.html',
                      {'searched': searched, 'book_by_author': book_by_author, 'book_by_name': book_by_name})

    return render(request, 'book/search.html', {})
