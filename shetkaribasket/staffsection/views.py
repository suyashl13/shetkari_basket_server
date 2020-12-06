from django.http.response import JsonResponse
from ..orders.models import Cart, Order
from ..orders.serializer import CartSerializer, OrderSerializer
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
@csrf_exempt
def process_undelivered_orders(request, u_id, token):
    try:
        UserModel = get_user_model()
        user = UserModel.objects.get(pk=u_id)
        if user.auth_token != token:
            return JsonResponse({"ERR": "Only users can see their orders"}, status=403)
        if user.is_staff != True:
            return JsonResponse({"ERR": "Only employees can take orders data"}, status=403)
    except:
        return JsonResponse({"ERR": "Invalid user"}, status=404)

    if request.method == 'GET':
        cart = Cart.objects.filter(is_delivered=False)
        serializer = CartSerializer(cart, many=True)
        return JsonResponse(serializer.data, safe=False)

    if request.method == 'POST':
        id = request.POST['cart_id']
        payment_method = request.POST['payment_method']
        is_delivered = request.POST['is_delivered']
        if is_delivered == "true":
            is_delivered = True
        else:
            is_delivered = False

        try:
            cart = Cart.objects.get(pk=id)
            cart.is_delivered = is_delivered
            cart.payment_method = payment_method
            cart.delivered_by = user
            cart.save()
            return JsonResponse(CartSerializer(cart).data, status=200)
        except:
            return JsonResponse({'ERR': "Cart does not exists"}, status=404)
