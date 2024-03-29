from django.urls import path
from .views import get_all_user_carts, make_order, cancel_cart, create_cart, get_user_cart_with_orders, verify_cart_order

urlpatterns = [
    path('get_user_carts/<int:u_id>/<str:token>/', get_all_user_carts),
    path('make_order/<int:u_id>/<str:token>/', make_order),
    path('cancel_cart/<int:cart_id>/<int:u_id>/<str:token>/', cancel_cart),
    path('create_cart/<int:u_id>/<str:token>/', create_cart),
    path('get_user_cart_with_orders/<int:cart_id>/<int:u_id>/<str:token>/', get_user_cart_with_orders),
    path('verify_cart_order/<int:cart_id>/<int:u_id>/<str:token>/', verify_cart_order),
]
