from django.http.response import JsonResponse


# Create your views here.
def api_home(request):
    return JsonResponse({
        "INFO": "API Home"
    })


def handler404(request, *args, **argv):
    return JsonResponse({"ERR": 'Page not found'}, status=404)
