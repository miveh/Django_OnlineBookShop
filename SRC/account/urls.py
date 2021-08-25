from django.urls import path
from .views import SignUpView, UserEditView, CreateAddressView, StaffPanel

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('edit/', UserEditView.as_view(), name='edit_profile'),
    path('address/', CreateAddressView.as_view(), name='address'),
    path('staff/', StaffPanel.as_view(), name='staff'),
]
