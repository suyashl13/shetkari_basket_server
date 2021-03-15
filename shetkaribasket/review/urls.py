from django.urls import path, include
from .views import make_review

urlpatterns = [
    path('<int:cart_id>/', make_review)
]