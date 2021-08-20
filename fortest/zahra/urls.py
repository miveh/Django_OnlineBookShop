from django.urls import path, include

from zahra.views import add_to

urlpatterns = [
    path('add_to/', add_to, name='addcart1'),
]
