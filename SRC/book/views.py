from django.shortcuts import render
from django.views.generic import ListView, DetailView
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


def search_bar(request):
    if request.method == 'POST':
        searched = request.POST['searched']
        result = Book.objects.filter(name__contains=searched)
        return render(request, 'book/search.html', {'searched': searched, 'result':result})
    return render(request, 'book/search.html', {})
