from django.urls import path
from book.views import AllBooksView, BookDetailView, CategoryBooksPageView, search_bar, \
    BookCreationView, CategoryCreationView, StoreroomView, BookEditView, BookDeleteView

urlpatterns = [
    path('search/', search_bar, name='search'),
    path('books', AllBooksView.as_view(), name='books'),
    path('book_details/<slug>', BookDetailView.as_view(), name='book_detail'),
    path('category_books/<slug>', CategoryBooksPageView.as_view(), name='category_books'),
    path('staff/add_book/', BookCreationView.as_view(), name='staff_add_book'),
    path('staff/add_category/', CategoryCreationView.as_view(), name='staff_add_category'),
    path('staff/storeroom/', StoreroomView.as_view(), name='storeroom'),
    path('staff/book/edit/<slug>', BookEditView.as_view(), name='book_edit'),
    path('staff/book/delete/<slug>', BookDeleteView.as_view(), name='book_delete'),
]
