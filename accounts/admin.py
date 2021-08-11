from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


# Register your models here.
from accounts.models import MyUser


class UserAdmin(BaseUserAdmin):
    list_display = ['id', 'date_of_birth', 'email', 'is_staff', 'is_active']
    model = MyUser
    ordering = ('id',)


admin.site.register(MyUser, UserAdmin)
