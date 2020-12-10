from django.urls import path
from .views import get_all_products, discounted_products, search_products

urlpatterns = [
    path('', get_all_products),
    path('discounted_products/', discounted_products),
    path('search_products/<str:p_name>/', search_products),
]
