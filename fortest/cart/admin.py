from django.contrib import admin

# Register your models here.
from cart.models import CartItems, Cart, FinalizedOrders

admin.site.register(CartItems)
admin.site.register(Cart)
admin.site.register(FinalizedOrders)