from django.urls import path
from .views import SignUpView, AddressEditView, UserEditView, CreateAddressView, StaffPanel, CustomerView, \
    my_address_view, AddressDeleteView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('profile/edit/', UserEditView.as_view(), name='edit_profile'),
    path('profile/address/', CreateAddressView.as_view(), name='address'),
    path('profile/my_addresses/', my_address_view, name='my_addresses'),
    path('staff/', StaffPanel.as_view(), name='staff'),
    path('staff/customers/', CustomerView.as_view(), name='customers'),
    path('staff/book/delete/<int:pk>', AddressDeleteView.as_view(), name='address_delete'),
    path('profile/address/edit/<int:pk>', AddressEditView.as_view(), name='address_edit'),
]
