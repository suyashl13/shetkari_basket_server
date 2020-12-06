from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .serializer import AnnouncementSerializer
from .models import Announcement


# Create your views here.
@csrf_exempt
def announcements(request):
    if request.method != 'GET':
        return JsonResponse({'ERR': 'Only GET requests are allowed.'}, status=400)

    try:
        all_announcements = Announcement.objects.all()
        serializer = AnnouncementSerializer(all_announcements, many=True)
        return JsonResponse(serializer.data, safe=False, status=200)
    except:
        return JsonResponse({'ERR': 'Internal server error'}, status=500)
