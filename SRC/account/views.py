from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, TemplateView
from account.forms import CustomUserCreationForm, CustomUserChangeForm, AddressForm
from account.models import ShippingAddress, CustomUser
from django.contrib.auth.mixins import LoginRequiredMixin


class SignUpView(CreateView):
    """
    این کلاس برای ثبت نام مشتری ها طراحی شده
    """

    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        """
        اطلاعات آدرس از فیلد های اضافه ی فرم گرفته و یک آدرس اصلی برای کاربر ذخیره می شود.
        :param form: اطلاعات هر کاربر هنگام ثبت نام در سایت
        :return: یه چیز الکی برای نداشتن ارور
        """

        try:
            form.save()
            user = CustomUser.objects.get(email=form.cleaned_data['email'])
            default_address = ShippingAddress.objects.create(user=user, city=form.cleaned_data['default_city'],
                                                             address=form.cleaned_data['default_address'],
                                                             default_address=True)
            default_address.save()
        except Exception as error:
            print("Oops! An exception has occurred:", error)

        return super(SignUpView, self).form_valid(form)


class UserEditView(UpdateView):
    form_class = CustomUserChangeForm
    template_name = 'profile/edit_profile.html'
    success_url = reverse_lazy('home')

    def get_object(self, queryset=None):
        return self.request.user


class CreateAddressView(LoginRequiredMixin, CreateView):
    """
    ااین ویو برای ذخیره آدرس جدید ایجاد شده.
    """

    form_class = AddressForm
    template_name = 'profile/address_form.html'
    success_url = reverse_lazy('edit_profile')

    def form_valid(self, form):
        """
        ا یک آدرس غیر اصلی برای کاربر ذخیره می شود
        :param form: اطلاعات فرم آدرس
        :return: یه چیز الکی برای نداشتن ارور
        """

        try:
            user = self.request.user
            print(user)
            address = ShippingAddress.objects.create(user=user, city=form.cleaned_data['city'],
                                                     address=form.cleaned_data['address'],
                                                     default_address=False)
            address.save()
        except Exception as error:
            print(f'user is: {self.request.user}')
            print("Oops! An exception has occurred:  {self.request.user}", error)

        return super().form_valid(form)


class StaffPanel(TemplateView):
    """
    پنل کارمند
    """
    template_name = "staff/staff.html"
