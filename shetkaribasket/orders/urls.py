from django.urls import path
from .views import get_user_carts, make_order, cancel_cart, create_cart

urlpatterns = [
    path('get_user_carts/<int:u_id>/<str:token>/', get_user_carts),
    path('make_order/<int:u_id>/<str:token>/', make_order),
    path('cancel_cart/<int:cart_id>/<int:u_id>/<str:token>/', cancel_cart),
    path('create_cart/<int:u_id>/<str:token>/', create_cart)
]