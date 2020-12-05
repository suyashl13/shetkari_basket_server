from django.urls import path, include
from .views import api_home

urlpatterns = [
    path('', api_home),
    path('users/', include('shetkaribasket.users.urls')),
    path('products/', include('shetkaribasket.products.urls')),
    path('orders/', include('shetkaribasket.orders.urls')),
]
