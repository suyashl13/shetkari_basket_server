from .serializer import UserSerializers
from django.contrib.auth import get_user_model
from django.contrib.auth import login, logout
from django.http.response import JsonResponse
import random
import string
from rest_framework.permissions import AllowAny
from rest_framework import viewsets
from django.views.decorators.csrf import csrf_exempt
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

    try:
        username = int(username)
        username = str(username)
    except:
        return JsonResponse({'ERR': 'Phone no. should be number.'}, status=400)

    if len(password) < 4:
        return JsonResponse({"ERR": "Password must be longer than 4 characters"}, status=400)

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
        return JsonResponse({'error': 'Invalid User id'}, status=404)
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
            return JsonResponse({"ERR": "Invalid User"}, status=404)
    else:
        return JsonResponse({"ERR": "Only GET request allowed"}, status=400)


@csrf_exempt
def check_token(request, u_id, token):
    if request.method != "GET":
        return JsonResponse({"ERR": "Only POST request allowed"}, status=400)

    try:
        UserModel = get_user_model()
        user = UserModel.objects.get(pk=u_id)
        if user.auth_token != token:
            return JsonResponse({"INFO": "Invalid token", 'result': False})
        else:
            return JsonResponse({"INFO": "Valid token", 'result': True})
    except:
        return JsonResponse({"ERR": "Invalid user"}, status=404)


def check_user(request, phone_number):
    if request.method != "GET":
        return JsonResponse({"ERR": "Only POST request allowed"}, status=400)

    try:
        UserModel = get_user_model()
        user = UserModel.objects.get(phone=phone_number)
        return JsonResponse({'exists': True})
    except:
        return JsonResponse({'exists': False}, status=404)
