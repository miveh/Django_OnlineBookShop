from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, ShippingAddress
from django.forms.models import inlineformset_factory


class CustomUserCreationForm(UserCreationForm):
    """
    این مدل برای ثبت نام کاربران ایجاد شده است
    """

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'national_code', 'email']

    default_city = forms.CharField(max_length=40, widget=forms.TextInput(), label='شهر')
    default_address = forms.CharField(max_length=300, widget=forms.TextInput(), label='محله، خیابان، کوچه...')
    use_required_attribute = ['national_code', 'first_name', 'last_name', 'default_city', 'default_address']


class CustomUserChangeForm(UserChangeForm):
    """
    این مدل یک فرم برای ویرایش مشخصات کاربران ایجاد می کند.
    """

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'national_code']


class AddressForm(forms.ModelForm):
    """
    این مدل یک فرم برای گرفتن آدرس جدید از مشتری ایجاد می کند.
    """

    class Meta:
        model = ShippingAddress
        fields = ['city', 'address']
