from django.urls import path
from book.views import AllBooksView, BookDetailView, CategoryBooksPageView, search_bar

urlpatterns = [
    path('search/', search_bar, name='search'),
    path('books', AllBooksView.as_view(), name='books'),
    path('book_details/<slug>', BookDetailView.as_view(), name='book_detail'),
    path('category_books/<slug>', CategoryBooksPageView.as_view(), name='category_books'),
]
