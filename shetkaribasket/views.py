from django.http.response import JsonResponse


# Create your views here.
def api_home(request):
    return JsonResponse({
        "INFO" : "API Home"
    })