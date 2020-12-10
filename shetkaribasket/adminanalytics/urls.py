from django.urls import path
from .views import get_todays_orders, get_undelivered_orders, get_total_sales, signin, get_all_orders

urlpatterns = [
    path('get_todays_orders/<int:u_id>/<str:token>/', get_todays_orders),
    path('get_undelivered_orders/<int:u_id>/<str:token>/', get_undelivered_orders),
    path('get_total_sales/<int:u_id>/<str:token>/', get_total_sales),
    path('get_all_orders/<int:u_id>/<str:token>/', get_all_orders),
    path('staff_login/', signin),
]
