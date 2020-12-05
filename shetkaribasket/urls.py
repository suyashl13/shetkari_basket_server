from django.urls import path, include
from . views import api_home

urlpatterns = [
    path('users/', include('shetkaribasket.users.urls')),
    path('', api_home),
]