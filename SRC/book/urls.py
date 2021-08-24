from django.urls import path
from book.views import AllBooksView, BookDetailView, CategoryBooksPageView

urlpatterns = [
    path('books', AllBooksView.as_view(), name='books'),
    path('book_details/<slug>', BookDetailView.as_view(), name='book_detail'),
    path('category_books/<slug>', CategoryBooksPageView.as_view(), name='category_books'),
]
