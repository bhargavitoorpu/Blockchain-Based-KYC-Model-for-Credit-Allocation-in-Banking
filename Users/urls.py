from django.urls import path
from Users.views import *

urlpatterns = [
    path('userhome/', userhome, name='userhome'),
    path('add_customer/', add_customer, name='add_customer'),
    path('customer_list/', customer_list, name='customer_list'),
    path('customer/<str:national_id>/blockchain/', view_blockchain_customer, name='view_blockchain_customer'),

]