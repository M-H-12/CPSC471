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
            target = Course.objects.get(pk=content['course_id'])
        except Course.DoesNotExist:
            return JsonResponse({"error": "Your prerequisite or course does not exist."})
        setattr(prereq, "prerequisite", target)
        prereq.full_clean()
        prereq.save()
        return JsonResponse({'response': "success", 'content': target.json_data(include_prerequisites=True)})

    if request.method == "DELETE":
        try:
            prereq = Course.objects.get(pk=content['prerequisite_id'])
        except Course.DoesNotExist:
            return JsonResponse({"error": "Course with course_id "
                                          + str(content['prerequisite_id']) + " does not exist."})
        prereq.prerequisite = None
        prereq.full_clean()
        prereq.save()
        return JsonResponse({'response': str(prereq.course_name) + ' has been removed as a prerequisite.'})

    response = JsonResponse({'error': "Request not met."})
    response.status_code = 405
    return response


"""
@csrf_exempt
def assignment(request):
    try:
        content = json.loads(request.body)['content']
    except KeyError:
        return JsonResponse({"error": "Please wrap your request body with 'content' "})

    if request.method == "GET":
        try:
            assignment = Assignment.objects.get(pk=content['assign_no'])
            return JsonResponse({"response": assignment.json_data()})
        except Assignment.DoesNotExist:
            return JsonResponse(
                {"error": "Assignment with assign_no " + str(content['assign_no']) + " does not exist."})

    if request.method == "POST":
        try:  # TODO Find out if this works
            assignment = Assignment.objects.create(**content)
            assignment.full_clean()
            assignment.save()
            return JsonResponse({"response": assignment.json_data()})
        except ValidationError as e:
            assignment.delete()
            return JsonResponse({'error': e.message_dict})
        except IntegrityError:
            return JsonResponse({'error': "Object could not be created."})

    if request.method == "DELETE":
        try:
            assignment = Assignment.objects.get(pk=content['assign_no'])
            assignment.delete()
            return JsonResponse({'response': 'success'})
        except Assignment.DoesNotExist:
            return JsonResponse(
                {"error": "Assignment with assign_no " + str(content['assign_no']) + " does not exist."})
        except ProtectedError:
            return {'error': "Couldn't delete object " + str(instance.id)}

    response = JsonResponse({'error': "Request not met."})
    response.status_code = 405
    return response

"""

"""

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import json
from . import models
from django.views.decorators.csrf import csrf_exempt


# Create your views here.

@csrf_exempt 
def admin(request):
    content = json.loads(request.body)['content']

    if request.method == "GET":
        try:
            administrator = Admin.objects.get(pk=content['sin'])
            return JsonResponse({"response" :administator.json_data()})
        except Admin.DoesNotExist:
            return JsonResponse({"error": "Admin with sin " + str(content['sin']) + " does not exist."})

    if request.method == "POST":
        try:
            administrator = Admin.objects.create(**content)
            administrator.full_clean()
            administrator.save()
            return JsonResponse({"response" :administator.json_data()})
        except ValidationError as e:
            administator.delete()
            return JsonResponse({'error': e.message_dict})
        except IntegrityError:
            return JsonResponse({'error': "Object could not be created."})

    if request.method == "DELETE":
        try:
            administrator = Admin.objects.get(pk=content['sin'])
            administator.delete()
            return JsonResponse({'response': 'success'})
        except Admin.DoesNotExist:
            return JsonResponse({"error": "Admin with sin " + str(content['sin']) + " does not exist."})
        except ProtectedError:
            return {'error': "Couldn't delete object " + str(instance.id)}

    response = JsonResponse({'error': "Request not met."})
    response.status_code = 405
    return response

@csrf_exempt 
def assignment(request):
    content = json.loads(request.body)['content']

    if request.method == "GET":
        try:
            assignment = Assignment.objects.get(pk=content['assign_no'])
            return JsonResponse({"response" :assignment.json_data()})
        except Assignment.DoesNotExist:
            return JsonResponse({"error": "Assignment with assign_no " + str(content['assign_no']) + " does not exist."})

    if request.method == "POST":
        try: #TODO Find out if this works
            assignment = Assignment.objects.create(**content)
            assignment.full_clean()
            assignment.save()
            return JsonResponse({"response" :assignment.json_data()})
        except ValidationError as e:
            assignment.delete()
            return JsonResponse({'error': e.message_dict})
        except IntegrityError:
            return JsonResponse({'error': "Object could not be created."})

    if request.method == "DELETE":
        try:
            assignment = Assignment.objects.get(pk=content['assign_no'])
            assignment.delete()
            return JsonResponse({'response': 'success'})
        except Assignment.DoesNotExist:
            return JsonResponse({"error": "Assignment with assign_no " + str(content['assign_no']) + " does not exist."})
        except ProtectedError:
            return {'error': "Couldn't delete object " + str(instance.id)}

    response = JsonResponse({'error': "Request not met."})
    response.status_code = 405
    return response


@csrf_exempt 
def material(request):
    content = json.loads(request.body)['content']

    if request.method == "GET":
        try:
            material = Material.objects.get(pk=content['material_no'])
            return JsonResponse({"response" :material.json_data()})
        except Material.DoesNotExist:
            return JsonResponse({"error": "Material with material_no " + str(content['material_no']) + " does not exist."})

    if request.method == "POST":
        try: #TODO Find out if this works
            material = Material.objects.create(**content)
            material.full_clean()
            material.save()
            return JsonResponse({"response" :material.json_data()})
        except ValidationError as e:
            material.delete()
            return JsonResponse({'error': e.message_dict})
        except IntegrityError:
            return JsonResponse({'error': "Object could not be created."})

    if request.method == "DELETE":
        try:
            material = Material.objects.get(pk=content['material_no'])
            material.delete()
            return JsonResponse({'response': 'success'})
        except Material.DoesNotExist:
            return JsonResponse({"error": "Material with material_no " + str(content['material_no']) + " does not exist."})
        except ProtectedError:
            return {'error': "Couldn't delete object " + str(instance.id)}

    response = JsonResponse({'error': "Request not met."})
    response.status_code = 405
    return response

"""
