from django.urls import path, include

from cart.views import add_to_cart, CartView, remove_from_cart, check_ordered, check_unordered, success, plus_quantity,\
    minus_quantity, MyFactorsView,  OrderedFromCartView, calculate_price_coupon

# ,ordered_from_view

urlpatterns = [
    path('cart/', CartView.as_view(), name='cart'),
    path('ordered_from_cart/', OrderedFromCartView.as_view(), name='orderedcart'),
    path('my_factors/', MyFactorsView.as_view(), name='myfactors'),
    path('add_to_cart/<slug>', add_to_cart, name='addcart'),
    path('check_ordered/<slug>', check_ordered, name='ordered'),
    path('check_unordered/<slug>', check_unordered, name='unordered'),
    path('remove_from_cart/<slug>', remove_from_cart, name='cart_remove'),
    path('success/', success, name='success'),
    path('plus_quantity/<slug>', plus_quantity, name='plus_quantity'),
    path('minus_quantity/<slug>', minus_quantity, name='minus_quantity'),
    path('calculate_price_coupon/', calculate_price_coupon, name='calculate_price_coupon'),

]
