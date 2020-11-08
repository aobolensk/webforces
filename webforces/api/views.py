from django.http import JsonResponse
from django.contrib.auth.decorators import login_required


@login_required
def stats(request):
    stats = {
        "name": "webforces",
    }
    return JsonResponse(stats)
