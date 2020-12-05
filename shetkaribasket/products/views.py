from django.http.response import JsonResponse
from .serializer import ProductSerializer
from .models import Product
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
@csrf_exempt
def get_all_products(request):
    if request.method != "GET":
        return JsonResponse({"ERR": "Only get requests are allowed on this route"}, status=400)

    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True, context={'request': request})
    return JsonResponse(serializer.data, safe=False)

@csrf_exempt
def discounted_products(request):
    if request.method != "GET":
        return JsonResponse({"ERR": "Only get requests are allowed on this route"}, status=400)

    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True, context={'request': request})
    discounted_products_list = []
    for prod in serializer.data:
        item = dict(prod)
        if item['discount'] != 0:
            discounted_products_list.append(item)

    return JsonResponse(discounted_products_list, safe=False)