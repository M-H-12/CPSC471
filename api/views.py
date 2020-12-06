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


def student():
    inputInfo = json.loads(request.body)['content']
    if request.method == "GET":
        try:
            student1 = Student.objects.get(sin=inputInfo['sin'])
            return JsonResponse("response: "+student1.json_data())
        except Student.DoesNotExist:
            return JsonResponse("error: Student with SIN:"+str(content['sin'])+" does not exist.")
    if request.method == "PUT":
        student1 = Student.objects.get(sin=inputInfo['sin'], year=inputInfo['year'],
                                       grade_average=inputInfo['grade_average'],
                                       credits_received=inputInfo['credits_received'])
        student1.save()

    if request.method == "DELETE":
        try:
            student1 = Student.objects.get(sin=inputInfo['sin'])
            student1.delete()
            return JsonResponse("response: Success")
        except Student.DoesNotExist:
            return JsonResponse("error: Student with SIN: "+str(content['sin'])+" does not exist.")
        except ProtectedError:
            return JsonResponse("error: Cannot delete student "+str(instance.id))

    response = JsonResponse("error: Request not met.")
    response.status_code = 405
    return response


def textbook():
    inputInfo = json.loads(request.body)['content']
    if request.method == "GET":
        try:
            textbook1 = Textbook.objects.get(book_no=inputInfo['book_no'], isbn=inputInfo['isbn'])
            return JsonResponse("response: "+textbook1.json_data())
        except Textbook.DoesNotExist:
            return JsonResponse("error: Textbook with key:"+str(content['book_no'])+
                                ","+str(content['isbn'])+" does not exist.")

    if request.method == "PUT":
        textbook1 = Textbook.objects.get(book_no=inputInfo['book_no'], isbn=inputInfo['isbn'], title=inputInfo['title'],
                                         year=inputInfo['year'], edition=inputInfo['textbook'],
                                         course_id=inputInfo['course_id'], student_no=inputInfo['student_no'])
        textbook1.save()

    if request.method == "DELETE":
        try:
            textbook1 = Textbook.objects.get(book_no=inputInfo['book_no'], isbn=inputInfo['isbn'])
            textbook1.delete()
            return JsonResponse("response: Success")
        except Textbook.DoesNotExist:
            return JsonResponse("error: Textbook with key:" + str(content['book_no']) +
                                "," + str(content['isbn']) + " does not exist.")
        except ProtectedError:
            return JsonResponse("error: Cannot delete textbook " + str(instance.id))

    response = JsonResponse("error: Request not met.")
    response.status_code = 405
    return response
