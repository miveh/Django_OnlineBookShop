from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, DetailView

from book.models import Book, Category


class HomeView(ListView):
    model = Category
    template_name = '_base.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        # context_data['books'] = Book.objects.all()
        context_data['categories'] = Category.objects.get_not_null_category()
        return context_data


class BookListView(ListView):
    model = Book
    template_name = 'book/book_list.html'
    context_object_name = 'books'


class BookDetailView(DetailView):
    model = Book
    template_name = 'book/book_details.html'


class CategoryDetailView(DetailView):
    model = Category
    template_name = 'book/category_details.html'


def search_bar(request):
    if request.method == 'POST':
        searched = request.POST['searched']
        books = Book.objects.filter(name__contains=searched)
        return render(request, 'book/search.html', {'searched': searched, 'books':books})
    return render(request, 'book/search.html', {})
