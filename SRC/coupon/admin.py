from django.contrib import admin
from django.utils.html import format_html
from coupon.models import CartCoupon, BookCashCoupon, BookPercentCoupon


@admin.action(description='Mark as active')
def make_diactive(modeladmin, request, queryset):
    queryset.update(is_active=False)


@admin.register(CartCoupon)
class CartCouponAdmin(admin.ModelAdmin):
    """
    کاستومایز کردن جدول تخفیف سبد خرید
    """

    @admin.display(description='')
    def edit_btn(self, obj):
        return format_html(
            '<span class="button" style="background: orange">ویرایش</span>'
        )

    fields = ['code', 'valid_from', 'valid_to', 'is_active', 'discount_percent']
    list_display = ['code', 'valid_from', 'valid_to', 'is_active', 'discount_percent', 'edit_btn']
    search_fields = ['discount_percent']
    list_editable = ['is_active', 'discount_percent']
    list_display_links = ['edit_btn']
    actions = [make_diactive]


@admin.register(BookCashCoupon)
class BookCashCouponAdmin(admin.ModelAdmin):
    """
    کاستومایز کردن جدول تخفیف نقدی کتاب
    """

    @admin.display(description='')
    def edit_btn(self, obj):
        return format_html(
            '<span class="button" style="background: orange">ویرایش</span>'
        )

    fields = ['valid_from', 'valid_to', 'is_active', 'discount_price', 'books']
    list_display = ['valid_from', 'valid_to', 'is_active', 'discount_price', 'edit_btn']
    search_fields = ['discount_price']
    list_editable = ['is_active', 'discount_price']
    list_display_links = ['edit_btn']
    actions = [make_diactive]


@admin.register(BookPercentCoupon)
class BookPercentCouponAdmin(admin.ModelAdmin):
    """
    کاستومایز کردن جدول تخفیف درصدی کتاب
    """

    @admin.display(description='')
    def edit_btn(self, obj):
        return format_html(
            '<span class="button" style="background: orange">ویرایش</span>'
        )

    fields = ['valid_from', 'valid_to', 'is_active', 'discount_percent', 'books']
    list_display = ['valid_from', 'valid_to', 'is_active', 'discount_percent', 'edit_btn']
    search_fields = ['discount_price']
    list_editable = ['is_active', 'discount_percent']
    list_display_links = ['edit_btn']
    actions = [make_diactive]