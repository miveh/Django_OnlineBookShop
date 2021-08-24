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
        fields = ['email', 'first_name', 'last_name', 'national_code']

    default_city = forms.CharField(max_length=40, widget=forms.TextInput(attrs={'label': 'شهر'}))
    default_address = forms.CharField(max_length=300, widget=forms.TextInput(attrs={'label': 'آدرس'}))
    national_code = forms.CharField(max_length=10, min_length=10)
    use_required_attribute = ['national_code', 'first_name', 'last_name', 'default_city', 'default_address']


# AddressFormset = inlineformset_factory(CustomUser, ShippingAddress, extra=1, exclude=())


class CustomUserChangeForm(UserChangeForm):
    """
    این مدل یک فرم برای ویرایش مشخصات کاربران ایجاد می کند.
    """

    class Meta:
        model = CustomUser
        fields = '__all__'







class AddressForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ['city', 'address']
