from django.urls import path
from cart.views import CartView, add_to_cart, remove_from_cart, quantity, quantity_next_cart, NextCartView, \
    add_to_next_cart, return_to_cart, remove_from_next_cart, create_factor, save_coupon_to_factor, success, \
    return_all_to_cart, HistoryListView, anonymous_cart, add_to_session, anonymous_cart_remove

urlpatterns = [
    path('cart/', CartView.as_view(), name='cart'),
    path('anonymous_cart/',anonymous_cart, name='anonymous_cart'),
    path('next_cart/', NextCartView.as_view(), name='next_cart'),
    path('add_to_cart/<slug>', add_to_cart, name='add_to_cart'),
    path('add_to_next_cart/<slug>', add_to_next_cart, name='add_to_next_cart'),
    path('return_to_cart/<slug>', return_to_cart, name='return_to_cart'),
    path('return_all_to_cart/', return_all_to_cart, name='return_all_to_cart'),
    path('remove_from_cart/<slug>', remove_from_cart, name='cart_remove'),
    path('remove_from_next_cart/<slug>', remove_from_next_cart, name='remove_from_next_cart'),
    path('quantity/<slug>', quantity, name='quantity'),
    path('quantity_next_cart/<slug>', quantity_next_cart, name='quantity_next_cart'),
    path('payment/', create_factor, name='payment'),
    path('save_coupon_to_factor/', save_coupon_to_factor, name='save_coupon_to_factor'),
    path('success', success, name='success'),
    path('history', HistoryListView.as_view(), name='history'),
    path('add_to_session/<slug>', add_to_session, name='add_to_session'),
    path('anonymous_cart_remove/<slug>', anonymous_cart_remove, name='anonymous_cart_remove'),
]