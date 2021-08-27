from django.contrib import admin
from django.utils.html import format_html
from cart.models import Cart, CartItems, FinalizedOrders


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    """
    این کلاس برای نمایش سبد های خرید در ادمین پنل است.
    """

    @admin.display(description='')
    def edit_btn(self, obj):
        return format_html(
            '<span class="button" style="background: orange">ویرایش</span>'
        )

    fields = ['user']
    list_display = ['id', 'user', 'created', 'updated', 'edit_btn']
    search_fields = ['user', 'id']
    list_display_links = ['edit_btn']


@admin.register(CartItems)
class CartItemsAdmin(admin.ModelAdmin):
    """
    این کلاس برای نمایش سفارشات در ادمین پنل است.
    """

    @admin.display(description='')
    def edit_btn(self, obj):
        return format_html(
            '<span class="button" style="background: orange">ویرایش</span>'
        )

    fields = ['cart', 'book', 'quantity', 'ordered']
    list_display = ['id', 'cart', 'book', 'quantity', 'ordered', 'edit_btn']
    search_fields = ['cart', 'id', 'book']
    list_display_links = ['edit_btn']


@admin.register(FinalizedOrders)
class FinalizedOrderAdmin(admin.ModelAdmin):
    """
    این کلاس برای نمایش فاکتورها در ادمین پنل است.
    """

    @admin.display(description='')
    def edit_btn(self, obj):
        return format_html(
            '<span class="button" style="background: orange">ویرایش</span>'
        )

    fields = ['cart', 'shipping_address', 'discount', 'price', 'item', 'payment']
    list_display = ['cart', 'shipping_address', 'discount', 'price', 'factor_total_price', 'payment', 'edit_btn']
    search_fields = ['cart']
    list_display_links = ['edit_btn']
