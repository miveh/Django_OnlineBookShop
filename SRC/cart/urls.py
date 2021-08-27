from django.urls import path
from cart.views import CartView, add_to_cart

urlpatterns = [
    path('cart/', CartView.as_view(), name='cart'),
    path('add_to_cart/<slug>', add_to_cart, name='add_to_cart'),
]
