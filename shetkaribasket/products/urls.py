from django.urls import path
from .views import get_all_products, discounted_products

urlpatterns = [
    path('', get_all_products),
    path('discounted_products/', discounted_products)
]
