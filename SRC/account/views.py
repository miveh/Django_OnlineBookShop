from django.urls import reverse_lazy
from django.views.generic import CreateView
from account.forms import CustomUserCreationForm
from account.models import ShippingAddress, CustomUser


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
