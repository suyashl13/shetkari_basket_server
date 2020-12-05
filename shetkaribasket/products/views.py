from django.http.response import JsonResponse
from .serializer import ProductSerializer
from .models import Product
from django.contrib.auth import get_user_model


# Create your views here.
def get_all_products(request):
    if request.method != "GET":
        return JsonResponse({"ERR": "Only get requests are allowed on this route"}, status=400)

    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True, context={'request': request})
    return JsonResponse(serializer.data, safe=False)


def discounted_products(request):
    if request.method != "GET":
        return JsonResponse({"ERR": "Only get requests are allowed on this route"}, status=400)

    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True, context={'request': request})
    discounted_products_list = []
    for prod in serializer.data:
        item = dict(prod)
        if item['discount'] is not 0:
            discounted_products_list.append(item)
        print(item)
    return JsonResponse(discounted_products_list, safe=False)