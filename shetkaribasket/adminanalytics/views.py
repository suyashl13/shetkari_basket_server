from ..orders.serializer import CartSerializer, OrderSerializer
from ..orders.models import Cart, Order
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
from django.contrib.auth import get_user_model, logout, login
from ..users.views import generate_token
from django.utils.datetime_safe import date


# Create your views here.
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

        if user.is_superuser == False:
            return JsonResponse({'ERR': "Only superusers are allowed on this route."})

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


@csrf_exempt
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
def get_todays_orders(request, u_id, token):
    if request.method != 'GET':
        return JsonResponse({'ERR': "Only GET requests are allowed on this route."}, status=400)

    # User Validation
    try:
        UserModel = get_user_model()
        user = UserModel.objects.get(pk=u_id)
        if user.auth_token != token:
            return JsonResponse({"ERR": "Only users can see their orders"}, status=403)
        if user.is_superuser != True:
            return JsonResponse({"ERR": "Only employees can access this route"}, status=403)
    except:
        return JsonResponse({"ERR": "Invalid user"}, status=404)

    try:
        print(date.today())
        queryset = Cart.objects.filter(date_created=date.today())
        todays_orders = []
        for undelivered_cart in queryset:
            orders = Order.objects.filter(cart=undelivered_cart)
            for order in orders:
                order_dict = dict(OrderSerializer(order).data)
                order_dict['cart_id'] = order.cart.id
                order_dict['product_name'] = order.product.name
                order_dict['address'] = order.user.address
                order_dict['name'] = order.user.name
                order_dict['phone'] = order.user.phone
                order_dict['is_delivered'] = order.cart.is_delivered
                todays_orders.append(order_dict)
        return JsonResponse(todays_orders, status=200, safe=False)
    except:
        return JsonResponse({"ERR": "Internal server error"}, status=500)


@csrf_exempt
def get_undelivered_orders(request, u_id, token):
    if request.method != 'GET':
        return JsonResponse({'ERR': "Only GET requests are allowed on this route."}, status=400)

    # User Validation
    try:
        UserModel = get_user_model()
        user = UserModel.objects.get(pk=u_id)
        if user.auth_token != token:
            return JsonResponse({"ERR": "Only users can see their orders"}, status=403)
        if user.is_superuser != True:
            return JsonResponse({"ERR": "Only superusers can access this route"}, status=403)
    except:
        return JsonResponse({"ERR": "Invalid user"}, status=404)

    # GET Undelivered Orders
    try:
        undelivered_orders = []
        undelivered_carts = Cart.objects.filter(is_delivered=False)
        for undelivered_cart in undelivered_carts:
            orders = Order.objects.filter(cart=undelivered_cart)
            for order in orders:
                order_dict = dict(OrderSerializer(order).data)
                order_dict['cart_id'] = order.cart.id
                order_dict['product_name'] = order.product.name
                order_dict['unit'] = order.product.unit
                order_dict['address'] = order.user.address
                order_dict['name'] = order.user.name
                order_dict['phone'] = order.user.phone
                order_dict['is_delivered'] = order.cart.is_delivered
                undelivered_orders.append(order_dict)
        return JsonResponse(undelivered_orders, status=200, safe=False)
    except:
        return JsonResponse({'Internal server error'}, status=500)


def get_total_sales(request, u_id, token):
    if request.method != 'GET':
        return JsonResponse({'ERR': "Only GET requests are allowed on this route."}, status=400)

    try:
        UserModel = get_user_model()
        user = UserModel.objects.get(pk=u_id)
        if user.auth_token != token:
            return JsonResponse({"ERR": "Only users can see their orders"}, status=403)
        if user.is_superuser != True:
            return JsonResponse({"ERR": "Only superusers can access this route"}, status=403)
    except:
        return JsonResponse({"ERR": "Invalid user"}, status=404)

    try:
        cart_query = Cart.objects.filter(is_delivered=True)
        carts = CartSerializer(cart_query, many=True).data

        total_sales = 0
        for cart in carts:
            cart_dict = dict(cart)
            total_sales = total_sales + int(cart_dict['subtotal'])

        cart_query = Cart.objects.filter(is_delivered=False)
        carts = CartSerializer(cart_query, many=True).data

        to_deliver_cost = 0
        for cart in carts:
            cart_dict = dict(cart)
            to_deliver_cost = to_deliver_cost + int(cart_dict['subtotal'])

        return JsonResponse({"total_sales": total_sales,
                             'to_deliver_cost': to_deliver_cost}, status=200)
    except:
        return JsonResponse({"ERR": "Internal server error"}, status=500)


def get_all_orders(request, u_id, token):
    if request.method != 'GET':
        return JsonResponse({'ERR': "Only GET requests are allowed on this route."}, status=400)

    try:
        UserModel = get_user_model()
        user = UserModel.objects.get(pk=u_id)
        if user.auth_token != token:
            return JsonResponse({"ERR": "Only users can see their orders"}, status=403)
        if user.is_superuser != True:
            return JsonResponse({"ERR": "Only superusers can access this route"}, status=403)
    except:
        return JsonResponse({"ERR": "Invalid user"}, status=404)

    try:
        all_orders = []
        all_carts = Cart.objects.all()
        for undelivered_cart in all_carts:
            orders = Order.objects.filter(cart=undelivered_cart)
            for order in orders:
                order_dict = dict(OrderSerializer(order).data)
                order_dict['cart_id'] = order.cart.id
                order_dict['product_name'] = order.product.name
                order_dict['phone'] = order.user.phone
                order_dict['address'] = order.user.address
                order_dict['name'] = order.user.name
                order_dict['payment_method'] = order.cart.payment_method
                order_dict['is_delivered'] = order.cart.is_delivered
                all_orders.append(order_dict)
        return JsonResponse(all_orders, status=200, safe=False)
    except:
        return JsonResponse({'Internal server error'}, status=500)
