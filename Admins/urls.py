from django.urls import path
from Admins.views import *

urlpatterns = [
    path('adminhome/', adminhome, name='adminhome'),
    path('admin_update_userstatus/<int:user_id>/', admin_update_userstatus, name='admin_update_userstatus'),
    path('customer_lists/', customer_lists, name='customer_lists'),
    path('customer/<int:customer_id>/update-kyc/', update_kyc_status, name='update_kyc_status'),
    path('predict_loan/', predict_loan, name='predict_loan'),
]