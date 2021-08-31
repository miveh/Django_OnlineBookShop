from django.contrib import admin
from django.utils.html import format_html
from account.models import CustomUser, Customer, Staff, ShippingAddress


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    """
    این کلاس برای جدا کردن مشتریان از سایر کاربران است.
    """

    @admin.display(description='')
    def edit_btn(self, obj):
        return format_html(
            '<span class="button" style="background: orange">ویرایش</span>'
        )

    fields = ['email', 'password', 'first_name', 'last_name', 'national_code', 'is_staff', 'is_active',
              'is_anonymous_user', 'groups', 'user_permissions', 'device']

    list_display = ['email', 'is_active', 'is_anonymous_user', 'first_name', 'last_name', 'edit_btn']
    search_fields = ['email', 'first_name', 'last_name']
    date_hierarchy = 'last_login'
    list_editable = ['is_active', 'first_name', 'last_name']
    list_display_links = ['edit_btn']
    list_filter = ['is_active']

    def get_queryset(self, request):
        return CustomUser.objects.filter(is_staff=False)


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    """
    این کلاس برای جدا کردن کارمندان از سایر کاربران است.
    """

    @admin.display(description='')
    def edit_btn(self, obj):
        return format_html(
            '<span class="button" style="background: orange">ویرایش</span>'
        )

    fields = ['email', 'password', 'first_name', 'last_name', 'last_login', 'is_staff', 'is_active', 'groups',
              'user_permissions', 'device']
    list_display = ['email', 'is_staff', 'is_active', 'last_login', 'device', 'edit_btn']
    search_fields = ['email']
    list_editable = ['is_active', 'is_staff']
    list_display_links = ['edit_btn']
    list_filter = ['is_active']

    def get_queryset(self, request):
        return CustomUser.objects.filter(is_staff=True)


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    """
    این کلاس برای جدا کردن super users از سایر کاربران است.
    """

    list_display = ['email', 'is_active', 'last_login', 'device']

    def get_queryset(self, request):
        return CustomUser.objects.filter(is_superuser=True)


@admin.register(ShippingAddress)
class ShippingAddressAdmin(admin.ModelAdmin):
    """
    برای جدول آدرس ها
    """

    @admin.display(description='')
    def edit_btn(self, obj):
        return format_html(
            '<span class="button" style="background: orange">ویرایش</span>'
        )

    list_display = ['city', 'address', 'default_address', 'edit_btn']
    search_fields = ['city']
    list_display_links = ['edit_btn']
    list_filter = ['default_address']
