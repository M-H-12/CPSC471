from django.db.models import ProtectedError
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db.utils import IntegrityError
import json
import datetime
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
            return JsonResponse({"error": "No sin included"})

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
def Teacher(request):
    try:
        content = json.loads(request.body)['content']
    except KeyError:
        return JsonResponse({"error": "Please wrap your request body with 'content' "})
    
    if request.method == "GET":
        try:
            person = Person.objects.get(pk=content['sin'])
            teacher = Teacher.objects.get(person = person)
            return JsonResponse(teacher.Json_data())
        except Teacher.DoesNotExist:
            return JsonResponse({"error": "Teacher with sin " + str(content['sin']) + " does not exist."})
        except KeyError:
            return JsonResponse({"error": "No sin included"})
        
    if request.method == "POST":
        try:
            person = Person.objects.get(pk=content['sin'])
            teacher = Teacher.objects.get(**content, person = person)
            teacher.full_clean()
            teacher.save()
            return JsonResponse({"response": teacher.json_data()})
        except ValidationError as e:
            teacher.delete()
            return JsonResponse({'error': e.message_dict})
        except IntegrityError:
            return JsonResponse({'error': "Teacher could not be created."})
        
    if request.method == "DELETE":
        try:
            person = Person.objects.get(pk=content['sin'])
            teacher = Teacher.objects.get(person = person)
            teacher.delete()
            return JsonResponse({'response': str(teacher.name) + ' has been deleted.'})
        except Teacher.DoesNotExist:
            return JsonResponse({"error": "Teacher with sin " + str(content['sin']) + " does not exist."})

    response = JsonResponse({'error': "Request not met."})
    response.status_code = 405
    return response
    

@csrf_exempt
def offering(request):
    try:
        content = json.loads(request.body)['content']
    except KeyError:
        return JsonResponse({"error": "Please wrap your request body with 'content' "})
    
    if request.method == "GET":
        try:
            room = Room.object.create(pk=content['room_no'])
            course = Course.object.create(pk=content['course_id'])
            offering = Offering.object.create(room=room, course=course, pk=content['offering_no'])
            return JsonResponse(offering.Json_data())
        except Room.DoesNotExist:
            return JsonResponse({"error": "Room with #" + str(content['room_no']) + " does not exist."})
        except Course.DoesNotExist:
            return JsonResponse({"error": "Course with id " + str(content['course_id']) + " does not exist."})
        except Offering.DoesNotExist:
            return JsonResponse({"error": "Offering with id " + str(content['offering_no']) + " does not exist."})
        except KeyError:
            return JsonResponse({"error": "No offering_id included"})
    
    if request.method == "POST":
        try:
            room = Room.object.create(pk=content['room_no'])
            course = Course.object.create(pk=content['course_id'])
            offering = Offering.object.create(room=room, course=course, pk=content['offering_no'])
            offering.full_clean()
            offering.save()
            return JsonResponse({"response": offering.json_data()})
        except ValidationError as e:
            offering.delete()
            return JsonResponse({'error': e.message_dict})
        except IntegrityError:
            return JsonResponse({'error': "Offering could not be created."})
    
    if request.method == "DELETE":
        try:
            room = Room.object.create(pk=content['room_no'])
            course = Course.object.create(pk=content['course_id'])
            offering = Offering.object.create(room=room, course=course, pk=content['offering_no'])
            offering.delete()
            return JsonResponse({'response': str(offering.offering_no) + ' has been deleted.'})
        except Offering.DoesNotExist:
            return JsonResponse({"error": "Offering with #" + str(content['offering_no']) + " does not exist."})
            
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


@csrf_exempt
def admin(request):
    try:
        content = json.loads(request.body)['content']
    except KeyError:
        return JsonResponse({"error": "Please wrap your request body with 'content' "})

    if request.method == "POST":
        try:
            administrator = Admin.objects.create(**content)
            administrator.full_clean()
            administrator.save()
            return JsonResponse({"response": administrator.json_data()})
        except ValidationError as e:
            administrator.delete()
            return JsonResponse({'error': e.message_dict})

    if request.method == "PUT":
        try:
            administrator = Admin.objects.get(pk=content['sin'])
        except Admin.DoesNotExist:
            return JsonResponse({"error": "Admin with id: " + str(content['sin']) + " does not exist."})
        except KeyError:
            return JsonResponse({"error": "No sin included"})

        try:
            for attr, value in content.items():
                setattr(administrator, attr, value)
            administrator.full_clean()
            administrator.save()
            return JsonResponse({'response': "success", 'content': administrator.json_data()})
        except ValidationError as e:
            return JsonResponse({'error': e.message_dict})

    if request.method == "DELETE":
        try:
            administrator = Admin.objects.get(pk=content['sin'])
            administrator.delete()
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
    try:
        content = json.loads(request.body)['content']
    except KeyError:
        return JsonResponse({"error": "Please wrap your request body with 'content' "})

    if request.method == "GET":
        course = Course.objects.get(pk=content['course_id'])
        offering = Offering.objects.get(course=course, offering_no=content['offering_no'])
        assignment = Assignment.objects.get(offering=offering, assign_no=content['assign_no'])
        return JsonResponse({"response": assignment.json_data()})

    if request.method == "POST":
        try:
            course = Course.objects.get(pk=content['course_id'])
            offering = Offering.objects.get(course=course, offering_no=content['offering_no'])
            assignment = Assignment.objects.create(**content, offering=offering)
            assignment.full_clean()
            assignment.save()
            return JsonResponse({"response": assignment.json_data()})
        except ValidationError as e:
            assignment.delete()
            return JsonResponse({'error': e.message_dict})

    if request.method == "PUT":
        course = Course.objects.get(pk=content['course_id'])
        offering = Offering.objects.get(course=course, offering_no=content['offering_no'])
        assignment = Assignment.objects.get(offering=offering, assign_no=content['assign_no'])

        try:
            for attr, value in content.items():
                setattr(assignment, attr, value)
            assignment.full_clean()
            assignment.save()
            return JsonResponse({'response': "success", 'content': assignment.json_data(include_prerequisites=True)})
        except ValidationError as e:
            return JsonResponse({'error': e.message_dict})

    if request.method == "DELETE":
        course = Course.objects.get(pk=content['course_id'])
        offering = Offering.objects.get(course=course, offering_no=content['offering_no'])
        assignment = Assignment.objects.get(offering=offering, assign_no=content['assign_no'])
        assignment.delete()
        return JsonResponse({'response': 'success'})

    response = JsonResponse({'error': "Request not met."})
    response.status_code = 405
    return response


@csrf_exempt
def material(request):
    try:
        content = json.loads(request.body)['content']
    except KeyError:
        return JsonResponse({"error": "Please wrap your request body with 'content' "})

    if request.method == "GET":
        course = Course.objects.get(pk=content['course_id'])
        offering = Offering.objects.get(course=course, offering_no=content['offering_no'])
        material = Material.objects.get(offering=offering, assign_no=content['material_no'])
        return JsonResponse({"response": material.json_data()})

    if request.method == "POST":
        try:
            course = Course.objects.get(pk=content['course_id'])
            offering = Offering.objects.get(course=course, offering_no=content['offering_no'])
            material = Material.objects.create(**content, offering=offering)
            material.full_clean()
            material.save()
            return JsonResponse({"response": material.json_data()})
        except ValidationError as e:
            material.delete()
            return JsonResponse({'error': e.message_dict})

    if request.method == "PUT":
        course = Course.objects.get(pk=content['course_id'])
        offering = Offering.objects.get(course=course, offering_no=content['offering_no'])
        material = Material.objects.get(offering=offering, assign_no=content['material_no'])

        try:
            for attr, value in content.items():
                setattr(material, attr, value)
            material.full_clean()
            material.save()
            return JsonResponse({'response': "success", 'content': material.json_data(include_prerequisites=True)})
        except ValidationError as e:
            return JsonResponse({'error': e.message_dict})

    if request.method == "DELETE":
        course = Course.objects.get(pk=content['course_id'])
        offering = Offering.objects.get(course=course, offering_no=content['offering_no'])
        material = Material.objects.get(offering=offering, assign_no=content['material_no'])
        material.delete()
        return JsonResponse({'response': 'success'})

    response = JsonResponse({'error': "Request not met."})
    response.status_code = 405
    return response


@csrf_exempt
def student():
    inputInfo = json.loads(request.body)['content']
    if request.method == "GET":
        try:
            student1 = Student.objects.get(sin=inputInfo['sin'])
            return JsonResponse("response: " + student1.json_data())
        except Student.DoesNotExist:
            return JsonResponse("error: Student with SIN:" + str(content['sin']) + " does not exist.")

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
            return JsonResponse("error: Student with SIN: " + str(content['sin']) + " does not exist.")
        except ProtectedError:
            return JsonResponse("error: Cannot delete student " + str(instance.id))

    response = JsonResponse("error: Request not met.")
    response.status_code = 405
    return response


@csrf_exempt
def textbook():
    inputInfo = json.loads(request.body)['content']
    if request.method == "GET":
        try:
            textbook1 = Textbook.objects.get(book_no=inputInfo['book_no'], isbn=inputInfo['isbn'])
            return JsonResponse("response: " + textbook1.json_data())
        except Textbook.DoesNotExist:
            return JsonResponse("error: Textbook with key:" + str(content['book_no']) +
                                "," + str(content['isbn']) + " does not exist.")

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

@csrf_exempt
def counselor():
    try:
        content = json.loads(request.body)['content']
    except KeyError:
        return JsonResponse({"error": "Please wrap your request body with 'content' "})

    if request.method == "GET":
        try:
            counselor = Counselor.objects.get(pk=content['sin'])
            return JsonResponse({'response': "success", 'content': counselor.json_data()})
        except Counselor.DoesNotExist:
            return JsonResponse({"error": "Counselor with sin " + str(content['sin']) + " does not exist."})
        except KeyError:
            return JsonResponse({"error": "No id included"})

    if request.method == "POST":
        try:
            counselor = Counselor.objects.create(**content)
            counselor.full_clean()
            counselor.save()
            return JsonResponse({"response": counselor.json_data()})
        except ValidationError as e:
            counselor.delete() 
            return JsonResponse({'error': e.message_dict})
        except IntegrityError:
            return JsonResponse({'error': "Object could not be created."})

    if request.method == "PUT":
        try:
            counselor = Counselor.objects.get(pk=content['sin'])
        except Counselor.DoesNotExist:
            return JsonResponse({"error": "Counselor with sin " + str(content['sin']) + " does not exist."})
        except KeyError:
            return JsonResponse({"error": "No sin included"})

        try:
            for attr, value in content.items():
                setattr(counselor, attr, value)
            counselor.full_clean()
            counselor.save()
            return JsonResponse({'response': "success", 'content': counselor.json_data()})
        except ValidationError as e:
            return JsonResponse({'error': e.message_dict})

    if request.method == "DELETE":
        try:
            counselor = Counselor.objects.get(pk=content['sin'])
            counselor.delete()
            return JsonResponse({'response': str(counselor.name) + ' has been deleted.'})
        except Counselor.DoesNotExist:
            return JsonResponse({"error": "Counselor with sin " + str(content['sin']) + " does not exist."})

    response = JsonResponse({'error': "Request not met."})
    response.status_code = 405
    return response

@csrf_exempt
def room():
    try:
        content = json.loads(request.body)['content']
    except KeyError:
        return JsonResponse({"error": "Please wrap your request body with 'content' "})

    if request.method == "GET":
        room = Room.objects.get(pk=content['room_no'])
        return JsonResponse({"response": room.json_data()})

    if request.method == "POST":
        try:
            room = Room.objects.create(**content)
            room.full_clean()
            room.save()
            return JsonResponse({"response": room.json_data()})
        except ValidationError as e:
            room.delete()
            return JsonResponse({'error': e.message_dict})

    if request.method == "PUT":
        room = Room.objects.get(pk=content['room_no'])
        try:
            for attr, value in content.items():
                setattr(room, attr, value)
            room.full_clean()
            room.save()
            return JsonResponse({'response': "success", 'content': room.json_data()})
        except ValidationError as e:
            return JsonResponse({'error': e.message_dict})

    if request.method == "DELETE":
        room = Room.objects.get(pk=content['room_no'])
        room.delete()
        return JsonResponse({'response': 'success'})

    response = JsonResponse({'error': "Request not met."})
    response.status_code = 405
    return response
