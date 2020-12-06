from django.urls import path
from .views import process_undelivered_orders

urlpatterns = [
    path('process_undelivered_orders/<int:u_id>/<str:token>/', process_undelivered_orders)
]