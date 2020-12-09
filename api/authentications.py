from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
import json


def login_person(request):
    if request.method != "POST":
        return JsonResponse({"response": "please use post"})

    if request.user.is_authenticated:
        return JsonResponse({"response": "already logged in", "content": request.user.get_username()})

    content = json.loads(request.body)['content']
    user = authenticate(request, username=content['sin'], password=content['password'])
    if user is not None:
        login(request, user)
        return JsonResponse({"response": "user logged in"})
    else:
        return JsonResponse({"response": "user not found"})


def logout_person(request):
    logout(request)
    return JsonResponse({"response": "user logged out"})
