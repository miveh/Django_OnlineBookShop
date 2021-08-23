from django.contrib import admin
from django.utils.html import format_html
# Register your models here.
from account.models import CustomUser, Customer, Staff


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

    fields = ['email', 'password', 'first_name', 'last_name', 'national_code', 'is_staff', 'is_active', 'groups',
              'user_permissions']
    list_display = ['email', 'is_active', 'first_name', 'last_name', 'edit_btn']
    search_fields = ['email', 'first_name', 'last_name']
    date_hierarchy = 'last_login'
    list_editable = ['is_active']
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
              'user_permissions']
    list_display = ['email', 'is_staff', 'is_active', 'last_login', 'edit_btn']
    search_fields = ['email', 'first_name', 'last_name']
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
    list_display = ['email', 'is_active', 'last_login']

    def get_queryset(self, request):
        return CustomUser.objects.filter(is_superuser=True)
