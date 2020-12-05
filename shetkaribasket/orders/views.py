from django.http.response import JsonResponse
from .models import Product, Cart, Order
from .serializer import CartSerializer, OrderSerializer
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime


# Create your views here.
@csrf_exempt
def get_user_carts(request, u_id, token):
    if request.method != "GET":
        return JsonResponse({'ERR': "Only get requests are allowed here"}, status=400)

    # User Validation
    try:
        UserModel = get_user_model()
        user = UserModel.objects.get(pk=u_id)
        if user.auth_token != token:
            return JsonResponse({"ERR": "Only users can see their orders"}, status=403)
    except:
        return JsonResponse({"ERR": "Invalid user"}, status=404)

    try:
        carts = Cart.objects.filter(user_owner=user)
        serializer = CartSerializer(carts, many=True)
        return JsonResponse(serializer.data, safe=False, status=200)
    except:
        return JsonResponse({"ERR": "Internal server error."}, status=500)


@csrf_exempt
def make_order(request, u_id, token):
    if request.method != "POST":
        return JsonResponse({'ERR': "Only POST requests are allowed here"}, status=400)

    # Validate User.
    try:
        UserModel = get_user_model()
        user = UserModel.objects.get(pk=u_id)
        if user.auth_token != token:
            return JsonResponse({"ERR": "Only users can see their orders"}, status=403)
    except:
        return JsonResponse({"ERR": "Invalid user"}, status=404)

    cart_id = request.POST['cart_id']
    product_id = request.POST['product_id']
    product_quantity = request.POST['quantity']

    try:
        qunt = int(product_quantity)
        if qunt > 9:
            return JsonResponse({"ERR": "Quantity should be an integer between 1 to 9"}, status=400)
    except:
        return JsonResponse({"ERR": "Quantity should be an integer"}, status=400)

    # Cart verification.
    try:
        cart = Cart.objects.get(pk=cart_id)
        if cart.user_owner != user:
            return JsonResponse({"ERR": "This cart belongs to another user"}, status=400)
    except:
        return JsonResponse({"ERR": "Cart does not exist."}, status=404)

    # Product verification.
    try:
        product = Product.objects.get(pk=product_id)
    except:
        return JsonResponse({"ERR": "Product does not exists."}, status=404)

    try:
        order = Order()
        order.quantity = str(qunt)
        order.cart = cart
        order.product = product
        order.user = user
        order.user_phone = user.phone
        order.order_status = "Assigned"
        order.save()
        serializer = OrderSerializer(order)
        return JsonResponse(serializer.data, status=200)
    except:
        return JsonResponse({"ERR": "Unable to place order"}, status=500)


@csrf_exempt
def cancel_cart(request, cart_id, u_id, token):
    if request.method != "DELETE":
        return JsonResponse({'ERR': "Only DELETE requests are allowed here"}, status=400)

    # Validate User.
    try:
        UserModel = get_user_model()
        user = UserModel.objects.get(pk=u_id)
        if user.auth_token != token:
            return JsonResponse({"ERR": "Only users can see their orders"}, status=403)
    except:
        return JsonResponse({"ERR": "Invalid user"}, status=404)

    # Ownership check
    try:
        cart = Cart.objects.get(pk=cart_id)
        if cart.user_owner != user:
            return JsonResponse({"ERR": "Only owners can cancel their cart"}, status=403)
    except:
        return JsonResponse({"ERR": "Invalid order id."}, status=404)

    # TimeOut check
    time_created = cart.date_time_created
    time_created = str(time_created)
    res = time_created.split('.')[0].split(' ')
    ordered_time = datetime.strptime(res[0] + " " + res[1], "%Y-%m-%d %H:%M:%S")
    now_time = datetime.now()

    if now_time.date() != ordered_time.date():
        return JsonResponse({"ERR": "Order can be canceled within a same day."}, status=400)

    if now_time.hour > 17:
        return JsonResponse({"ERR": "Order can be canceled before 7 PM"}, status=400)

    if ordered_time.hour + 8 < now_time.hour:
        return JsonResponse({"ERR": "Order can be canceled only within 8 hours"}, status=400)

    # Cart cancellation algorithm
    try:
        orders = Order.objects.filter(cart=cart)
        for order in orders:
            order.delete()
        cart.delete()
        return JsonResponse({"INFO": "Cart cancelled successfully"}, status=200)

    except:
        return JsonResponse({"ERR": "Internal server error"}, status=500)


@csrf_exempt
def create_cart(request, u_id, token):
    if request.method != "POST":
        return JsonResponse({'ERR': "Only POST requests are allowed here"}, status=400)

    subtotal = request.POST['subtotal']

    try:
        subtotal = int(subtotal)
        subtotal = str(subtotal)
    except:
        return JsonResponse({"ERR": "subtotal must be integer"}, status=400)

    # Validate User.
    try:
        UserModel = get_user_model()
        user = UserModel.objects.get(pk=u_id)
        if user.auth_token != token:
            return JsonResponse({"ERR": "Invalid auth token"}, status=403)
    except:
        return JsonResponse({"ERR": "Invalid user"}, status=404)

    try:
        cart = Cart()
        cart.user_owner = user
        cart.subtotal = subtotal
        cart.user_address = user.address
        cart.save()
        print(user.address)
        return JsonResponse(CartSerializer(cart).data)
    except:
        return JsonResponse({'ERR': "Unable to create cart"}, status=500)
