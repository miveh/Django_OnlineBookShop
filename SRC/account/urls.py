from django.urls import path
from .views import SignUpView, UserEditView, CreateAddressView, StaffPanel, CustomerView, MyAddressView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('profile/edit/', UserEditView.as_view(), name='edit_profile'),
    path('profile/address/', CreateAddressView.as_view(), name='address'),
    path('profile/my_addresses/', MyAddressView.as_view(), name='my_addresses'),
    path('staff/', StaffPanel.as_view(), name='staff'),
    path('staff/customers/', CustomerView.as_view(), name='customers'),
]
