from django.urls import path
from .views import process_undelivered_orders, signin, get_orders_by_cart_id

urlpatterns = [
    path('process_undelivered_orders/<int:u_id>/<str:token>/', process_undelivered_orders),
    path('get_orders_by_cart_id/<int:cart_id>/<int:u_id>/<str:token>/', get_orders_by_cart_id),
    path('signin/', signin),
]