from django.http.response import JsonResponse
from rest_framework import status
from .models import Review
from ..orders.models import Cart
from ..orders.serializer import CartSerializer
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
@csrf_exempt
def make_review(request, cart_id):
    if request.method == "GET":
        try:
            r_cart = Cart.objects.get(pk=cart_id)
            rv = Review.objects.filter(review_cart=r_cart)
            if len(rv) != 0:
                return JsonResponse({"ERR": "Already reviewed!"}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return JsonResponse({"ERR": "Cart does not exist"}, status=status.HTTP_400_BAD_REQUEST)

        return JsonResponse(CartSerializer(r_cart).data)

    rating = request.POST['rating']
    comment = request.POST['comment']

    # Validations
    try:
        f_rating = float(rating)
    except:
        return JsonResponse({"ERR": "Rating should be a float"}, status=status.HTTP_400_BAD_REQUEST)
    if len(comment) > 255:
        return JsonResponse({"ERR": "Comment should be smaller than 255 words"}, status=status.HTTP_400_BAD_REQUEST)
    try:
        r_cart = Cart.objects.get(pk=cart_id)
        rv = Review.objects.filter(review_cart=r_cart)
        if len(rv) != 0:
            return JsonResponse({"ERR": "Already reviewed!"}, status=status.HTTP_400_BAD_REQUEST)
    except:
        return JsonResponse({"ERR": "cart_id should be a valid number."}, status=status.HTTP_400_BAD_REQUEST)

    # Do stuff
    try:
        r_cart = Cart.objects.get(pk=cart_id)
    except:
        return JsonResponse({"ERR": "cart not found"}, status=status.HTTP_404_NOT_FOUND)

    try:
        review = Review()
        review.review_cart = r_cart
        review.comment = comment
        review.rating = rating
        review.save()
        return JsonResponse({"INFO": "Reviewed successfully."}, status=200)
    except:
        return JsonResponse({"ERR": "cart not found"}, status=status.HTTP_404_NOT_FOUND)
