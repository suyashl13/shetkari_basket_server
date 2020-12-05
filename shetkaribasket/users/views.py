from .serializer import UserSerializers
from django.contrib.auth import get_user_model
from django.contrib.auth import login, logout
from django.http.response import JsonResponse
import random
import string
import re
from rest_framework.permissions import AllowAny
from rest_framework import viewsets
from django.views.decorators.csrf import csrf_exempt
from .models import CustomUser
from .serializer import UserSerializers


# Create your views here.
def generate_token():
    return ''.join(random.choice(string.ascii_lowercase) for i in range(10))


@csrf_exempt
def signin(request):
    if request.method != 'POST':
        return JsonResponse({"ERR": "Only POST method allowed"})

    username = request.POST['phone']
    password = request.POST['password']

    if len(password) < 4:
        return JsonResponse({"ERR": "Password must be longer than 4 characters"})

    usermodel = get_user_model()
    try:
        user = usermodel.objects.get(phone=username)
        if user.check_password(password):
            user_dict = usermodel.objects.filter(phone=int(username)).values().first()
            user_dict.pop('password')

            # if user.auth_token != "0":
            #     user.auth_token = "0"
            #     user.save()
            #     return JsonResponse({"ERR": "Previous session exists"})

            token = generate_token()
            user.auth_token = token
            user.save()
            login(request, user)
            return JsonResponse({'token': token, 'user': user_dict})
        else:
            return JsonResponse({
                'ERR': 'Invalid login credentials.'
            })
    except usermodel.DoesNotExist:
        return JsonResponse({"ERR": "Invalid user"})


class UserViewSet(viewsets.ModelViewSet):
    custom_user = get_user_model()
    permission_classes = [AllowAny]
    queryset = custom_user.objects.all()
    serializer_class = UserSerializers


def signout(request, id):
    UserModel = get_user_model()
    try:
        user = UserModel.objects.get(pk=id)
        user.auth_token = "0"
        user.save()
        logout(request)
    except UserModel.DoesNotExist:
        return JsonResponse({'error': 'Invalid User id'})
    return JsonResponse({'INFO': 'Logged out successfully'})


@csrf_exempt
def get_current_user(request):
    if not request.user.is_authenticated:
        return JsonResponse({"ERR": "User is not logged in."})
    if request.method == "GET":
        UserModel = get_user_model()
        try:
            user = request.user
            usr = UserModel.objects.get(email=user)
            serializer = UserSerializers(usr)
            return JsonResponse(serializer.data)
        except UserModel.DoesNotExist:
            return JsonResponse({"ERR": "Invalid User"})
    else:
        return JsonResponse({"ERR": "Only GET request allowed"})
