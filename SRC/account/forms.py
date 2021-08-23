from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    """
    این مدل برای ثبت نام کاربران ایجاد شده است
    """
    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'national_code']

    national_code = forms.CharField(max_length=10 ,min_length=10)
    use_required_attribute = ['national_code', 'first_name', 'last_name']


class CustomUserChangeForm(UserChangeForm):
    """
    این مدل یک فرم برای ویرایش مشخصات کاربران ایجاد می کند.
    """
    class Meta:
        model = CustomUser
        fields = '__all__'
