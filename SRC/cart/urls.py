from django.urls import path
from cart.views import CartView, add_to_cart, remove_from_cart, quantity, quantity_next_cart, NextCartView

urlpatterns = [
    path('cart/', CartView.as_view(), name='cart'),
    path('next_cart/', NextCartView.as_view(), name='next_cart'),
    path('add_to_cart/<slug>', add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<slug>', remove_from_cart, name='cart_remove'),
    path('quantity/<slug>', quantity, name='quantity'),
    path('quantity_next_cart/<slug>', quantity_next_cart, name='quantity_next_cart'),
]
