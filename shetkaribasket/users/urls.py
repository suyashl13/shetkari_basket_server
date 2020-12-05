from django.urls import path, include
from . views import signin, UserViewSet, signout, get_current_user
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'', UserViewSet)


urlpatterns = [
    path('signin/', signin),
    path('signout/<int:id>/', signout),
    path('current_user/', get_current_user),
    path('', include(router.urls)),
]