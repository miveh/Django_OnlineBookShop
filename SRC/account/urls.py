from django.urls import path
from .views import SignUpView, UserEditView, CreateAddressView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('edit/', UserEditView.as_view(), name='edit_profile'),
    path('address/', CreateAddressView.as_view(), name='address'),
]
