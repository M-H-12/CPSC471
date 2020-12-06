from django.db.models import ProtectedError
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db.utils import IntegrityError
import json
from .models import *


@csrf_exempt
def person(request):
    try:
        content = json.loads(request.body)['content']
    except KeyError:
        return JsonResponse({"error": "Please wrap your request body with 'content' "})

    if request.method == "GET":
        try:
            person = Person.objects.get(pk=content['sin'])
            return JsonResponse({'response': "success", 'content': person.json_data()})
        except Person.DoesNotExist:
            return JsonResponse({"error": "Person with sin " + str(content['sin']) + " does not exist."})
        except KeyError:
            return JsonResponse({"error": "No id included"})

    if request.method == "POST":
        try:
            person = Person.objects.create(**content)
            person.full_clean()
            person.save()
            return JsonResponse({"response": person.json_data()})
        except ValidationError as e:
            person.delete()  # FIXME if sin not provided, the object will still be created (we can't delete it)
            return JsonResponse({'error': e.message_dict})
        except IntegrityError:
            return JsonResponse({'error': "Object could not be created."})

    if request.method == "PUT":
        try:
            person = Person.objects.get(pk=content['sin'])
        except Person.DoesNotExist:
            return JsonResponse({"error": "Person with sin " + str(content['sin']) + " does not exist."})
        except KeyError:
            return JsonResponse({"error": "No id included"})

        try:
            for attr, value in content.items():
                setattr(person, attr, value)
            person.full_clean()
            person.save()
            return JsonResponse({'response': "success", 'content': person.json_data()})
        except ValidationError as e:
            return JsonResponse({'error': e.message_dict})

    if request.method == "DELETE":
        try:
            person = Person.objects.get(pk=content['sin'])
            person.delete()
            return JsonResponse({'response': str(person.name) + ' has been deleted.'})
        except Person.DoesNotExist:
            return JsonResponse({"error": "Person with sin " + str(content['sin']) + " does not exist."})

    response = JsonResponse({'error': "Request not met."})
    response.status_code = 405
    return response


@csrf_exempt
def course(request):
    try:
        content = json.loads(request.body)['content']
    except KeyError:
        return JsonResponse({"error": "Please wrap your request body with 'content' "})

    if request.method == "GET":
        try:
            course = Course.objects.get(pk=content['course_id'])
            return JsonResponse({"response": course.json_data(include_prerequisites=True)})
        except Course.DoesNotExist:
            return JsonResponse({"error": "Course with course_id " + str(content['course_id']) + " does not exist."})

    if request.method == "POST":
        try:
            course = Course.objects.create(**content)
            course.full_clean()
            course.save()
            return JsonResponse({"response": course.json_data(include_prerequisites=True)})
        except ValidationError as e:
            course.delete()
            return JsonResponse({'error': e.message_dict})
        except IntegrityError:
            return JsonResponse({'error': "Object could not be created."})

    if request.method == "PUT":
        try:
            course = Course.objects.get(pk=content['course_id'])
        except Course.DoesNotExist:
            return JsonResponse({"error": "Course with id " + str(content['course_id']) + " does not exist."})
        except KeyError:
            return JsonResponse({"error": "No id included"})

        try:
            for attr, value in content.items():
                setattr(course, attr, value)
            course.full_clean()
            course.save()
            return JsonResponse({'response': "success", 'content': course.json_data(include_prerequisites=True)})
        except ValidationError as e:
            return JsonResponse({'error': e.message_dict})

    if request.method == "DELETE":
        try:
            course = Course.objects.get(pk=content['course_id'])
            course.delete()
            return JsonResponse({'response': str(course.course_name) + ' has been deleted.'})
        except Course.DoesNotExist:
            return JsonResponse({"error": "Course with course_id " + str(content['course_id']) + " does not exist."})

    response = JsonResponse({'error': "Request not met."})
    response.status_code = 405
    return response


@csrf_exempt
def prerequisite(request):
    try:
        content = json.loads(request.body)['content']
    except KeyError:
        return JsonResponse({"error": "Please wrap your request body with 'content' "})

    if request.method == "PUT":
        try:
            prereq = Course.objects.get(pk=content['prerequisite_id'])
            parent = Course.objects.get(pk=content['parent_id'])
        except Course.DoesNotExist:
            return JsonResponse({"error": "Your prerequisite or parent course does not exist."})
        setattr(prereq, "parent", parent)
        prereq.full_clean()
        prereq.save()
        return JsonResponse({'response': "success", 'content': parent.json_data(include_prerequisites=True)})

    if request.method == "DELETE":
        try:
            prereq = Course.objects.get(pk=content['prerequisite_id'])
        except Course.DoesNotExist:
            return JsonResponse({"error": "Course with course_id "
                                          + str(content['prerequisite_id']) + " does not exist."})
        prereq.parent = None
        prereq.full_clean()
        prereq.save()
        return JsonResponse({'response': str(prereq.course_name) + ' has been removed as a prerequisite.'})

    response = JsonResponse({'error': "Request not met."})
    response.status_code = 405
    return response


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