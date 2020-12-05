from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import json
from . import models

# Create your views here.

def course_data(request):
    return HttpResponse("Hello, world. You're at the polls index.")
    #return JsonResponse()

def create_course(request):
    if request.method != "POST":
        response = JsonResponse({'error': 'This endpoint can only be accessed with POST'})
        response.status_code = 400
        return response

    content = json.loads(request.body)['content']
