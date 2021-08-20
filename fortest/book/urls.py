from django.urls import path

import book
from book.views import  HomeView, CategoryDetailView, BookListView, BookDetailView, search_bar
#
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('books/', BookListView.as_view(), name='booklist'),
    path('search/', search_bar, name='search'),
    path('book_details/<slug>', BookDetailView.as_view(), name='bookdetail'),
    # path('book_details/(?P<slug>[^/]+)$', BookDetailView.as_view(), name='bookdetail'),
    path('category_details/<slug>', CategoryDetailView.as_view(), name='categorydetail'),
]
