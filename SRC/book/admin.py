from django.contrib import admin
from django.utils.html import format_html
from book.models import Book, Category


@admin.action(description='no stock')
def make_no_stock(modeladmin, request, queryset):
    queryset.update(stock=0)


class CategoryInline(admin.TabularInline):
    model = Book.category.through


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """
    کاستومایز کردن جدول کتاب ها
    """

    @admin.display(description='')
    def edit_btn(self, obj):
        return format_html(
            '<span class="button" style="background: orange">ویرایش</span>'
        )

    fields = ['name', 'author', 'stock', 'price', 'image', 'description', 'category']
    list_display = ['name', 'author', 'stock', 'price', 'image', 'edit_btn']
    search_fields = ['name']
    list_editable = ['stock', 'price']
    list_display_links = ['edit_btn']
    actions = [make_no_stock]

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    کاستومایز کردن جدول دسته بندی ها
    """

    @admin.display(description='')
    def edit_btn(self, obj):
        return format_html(
            '<span class="button" style="background: orange">ویرایش</span>'
        )

    fields = ['category']
    list_display = ['category', 'edit_btn']
    search_fields = ['category']
    list_display_links = ['edit_btn']
    inlines = [CategoryInline]