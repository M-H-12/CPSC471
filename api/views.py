from django.db.models import ProtectedError
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db.utils import IntegrityError
from django.contrib.auth.models import Permission, User
from django.contrib.contenttypes.models import ContentType
import json
import datetime
from .models import *
# from builtins import None
from rest_framework.generics import ListAPIView, RetrieveAPIView
from .serializers import StudentSerializer


class StudentListView(ListAPIView):
    queyset = Student.objects.all()
    serializer_class = StudentSerializer


class StudentDetailView(RetrieveAPIView):
    queyset = Student.objects.all()
    serializer_class = StudentSerializer


# 1
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

    if request.method == "POST" and request.user.has_perm('api.change_admin'):
        try:
            course = Course.objects.create(**content)
            course.full_clean()
            course.save()
            return JsonResponse({'response': "success", 'content': course.json_data(include_prerequisites=True)})
        except ValidationError as e:
            course.delete()
            return JsonResponse({'error': e.message_dict})
        except IntegrityError:
            return JsonResponse({'error': "Object could not be created."})

    if request.method == "PUT" and request.user.has_perm('api.change_admin'):
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

    if request.method == "DELETE" and request.user.has_perm('api.change_admin'):
        try:
            course = Course.objects.get(pk=content['course_id'])
            course.delete()
            return JsonResponse({'response': str(course.course_name) + ' has been deleted.'})
        except Course.DoesNotExist:
            return JsonResponse({"error": "Course with course_id " + str(content['course_id']) + " does not exist."})

    response = JsonResponse({'error': "Request not met."})
    response.status_code = 405
    return response


# 2
def teacher_office_hours(request):
    content = json.loads(request.body)['content']

    if request.method == "POST" and request.user.has_perm('api.change_teacher'):
        teacher = Teacher.objects.get(pk=content['sin'])
        teacher_office_hour = TeacherOfficeHour.objects.create(teacher=teacher, day=content['day'],
                                                               hour_from=content['hour_from'],
                                                               hour_to=content['hour_to'])
        teacher_office_hour.full_clean()
        teacher_office_hour.save()
        return JsonResponse({'response': "success"})

    if request.method == "DELETE" and request.user.has_perm('api.change_teacher'):
        teacher = Teacher.objects.get(pk=content['sin'])
        teacher_office_hour = TeacherOfficeHour.objects.get(teacher=teacher, day=content['day'],
                                                            hour_from=content['hour_from'],
                                                            hour_to=content['hour_to'])
        teacher_office_hour.delete()
        return JsonResponse({'response': "success"})

    response = JsonResponse({'error': "Request not met."})
    response.status_code = 405
    return response


# 3
def teacher_can_teach(request):
    try:
        content = json.loads(request.body)['content']
    except KeyError:
        return JsonResponse({"error": "Please wrap your request body with 'content' "})

    course = Course.objects.get(pk=content['course_id'])
    teacher = Teacher.objects.get(pk=content['sin'])

    if request.method == "PUT" and request.user.has_perm('api.change_teacher'):
        teacher.can_teach.add(course)
        teacher.full_clean()
        teacher.save()
        return JsonResponse({'response': "success", 'content': teacher.json_data()})

    if request.method == "DELETE" and request.user.has_perm('api.change_teacher'):
        teacher.can_teach.remove(course)
        teacher.full_clean()
        teacher.save()
        return JsonResponse({'response': "success", 'content': teacher.json_data()})

    response = JsonResponse({'error': "Request not met."})
    response.status_code = 405
    return response


# 4
def course_textbook(request):
    try:
        content = json.loads(request.body)['content']
    except KeyError:
        return JsonResponse({"error": "Please wrap your request body with 'content' "})

    if request.method == "PUT" and request.user.has_perm('api.change_teacher'):
        course = Course.objects.get(pk=content['course_id'])
        textbook = Textbook.objects.get(isbn=content['isbn'])
        setattr(textbook, "course", course)
        textbook.full_clean()
        textbook.save()
        return JsonResponse({'response': "success", 'content': course.json_data(include_prerequisites=False)})

    if request.method == "DELETE" and request.user.has_perm('api.change_teacher'):
        course = Course.objects.get(pk=content['course_id'])
        textbook = Textbook.objects.get(isbn=content['isbn'])
        course.required_textbooks.remove(textbook)
        course.full_clean()
        course.save()
        return JsonResponse({'response': "success", 'content': course.json_data(include_prerequisites=False)})

    response = JsonResponse({'error': "Request not met."})
    response.status_code = 405
    return response4


# 1
def teacher(request):
    try:
        content = json.loads(request.body)['content']
    except KeyError:
        return JsonResponse({"error": "Please wrap your request body with 'content' "})

    if request.method == "GET":
        person = Teacher.objects.get(pk=content['sin'])
        return JsonResponse({'response': "success", 'content': person.json_data()})

    if request.method == "PUT" and request.user.has_perm('api.change_admin'):
        person = Teacher.objects.get(pk=content['sin'])

        for attr, value in content.items():
            setattr(person, attr, value)
        person.full_clean()
        person.save()
        return JsonResponse({'response': "success", 'content': person.json_data()})

    if request.method == "DELETE" and request.user.has_perm('api.change_admin'):
        person = Teacher.objects.get(pk=content['sin'])
        person.delete()
        User.objects.get(username=content['sin']).delete()
        return JsonResponse({'response': str(person.name) + ' has been deleted.'})

    if request.method == "POST" and request.user.has_perm('api.change_admin'):
        try:
            teacher = Teacher.objects.create(**content)
            teacher.full_clean()
            teacher.save()

            content_type1 = ContentType.objects.get_for_model(Teacher)
            content_type3 = ContentType.objects.get_for_model(Student)
            permission1 = Permission.objects.get(
                codename='change_teacher',
                content_type=content_type1,
            )
            permission3 = Permission.objects.get(
                codename='change_student',
                content_type=content_type3,
            )
            user = User.objects.create_user(username=content['sin'], password=content['password'])
            user.user_permissions.add(permission1)
            user.user_permissions.add(permission3)

            return JsonResponse({'response': "success", "content": teacher.json_data()})
        except ValidationError as e:
            teacher.delete()
            return JsonResponse({'error': e.message_dict})
        except IntegrityError:
            return JsonResponse({'error': "Teacher could not be created."})

    response = JsonResponse({'error': "Request not met."})
    response.status_code = 405
    return response


# 2
def offering_room(request):
    content = json.loads(request.body)['content']

    if request.method == "DELETE" and request.user.has_perm('api.change_teacher'):
        course = Course.objects.get(pk=content['course_id'])
        offering = Offering.objects.get(course=course, offering_no=content['offering_no'])
        offering.room = None
        offering.delete()
        return JsonResponse({'response': 'success', 'content': room.json_data()})

    if request.method == "PUT" and request.user.has_perm('api.change_teacher'):
        course = Course.objects.get(pk=content['course_id'])
        offering = Offering.objects.get(course=course, offering_no=content['offering_no'])
        room = Room.objects.get(pk=content['room_no'])
        offering.room = room
        offering.full_clean()
        offering.save()
        return JsonResponse({'response': 'Success', 'content': room.json_data()})

    response = JsonResponse({'error': "Request not met."})
    response.status_code = 405
    return response


# 3
def offering_time(request):
    content = json.loads(request.body)['content']

    course = Course.objects.get(pk=content['course_id'])
    offering = Offering.objects.get(course=course, offering_no=content['offering_no'])

    if request.method == "POST" and request.user.has_perm('api.change_teacher'):
        offering_time = OfferingDayAndTime.objects.create(offering=offering,
                                                          day=content['day'],
                                                          hour_from=content['hour_from'],
                                                          hour_to=content['hour_to'])
        offering_time.full_clean()
        offering_time.save()
        return JsonResponse({'response': 'offering_time created', 'content': offering.json_data(True)})

    if request.method == "DELETE" and request.user.has_perm('api.change_teacher'):
        offering_time = OfferingDayAndTime.objects.get(offering=offering,
                                                       day=content['day'],
                                                       hour_from=content['hour_from'],
                                                       hour_to=content['hour_to'])
        offering_time.delete()
        return JsonResponse({'response': 'offering_time deleted', 'content': offering.json_data(True)})

    response = JsonResponse({"error": "request not met."})
    response.status_code = 405
    return response


# 4
def offering(request):
    try:
        content = json.loads(request.body)['content']
    except KeyError:
        return JsonResponse({"error": "Please wrap your request body with 'content' "})

    if request.method == "GET":
        try:
            course = Course.objects.get(pk=content['course_id'])
            offering = Offering.objects.get(course=course, offering_no=content['offering_no'])
            return JsonResponse(offering.json_data(True))
        except Room.DoesNotExist:
            return JsonResponse({"error": "Room with #" + str(content['room_no']) + " does not exist."})
        except Course.DoesNotExist:
            return JsonResponse({"error": "Course with id " + str(content['course_id']) + " does not exist."})
        except Offering.DoesNotExist:
            return JsonResponse({"error": "Offering with id " + str(content['offering_no']) + " does not exist."})
        except KeyError:
            return JsonResponse({"error": "No offering_id included"})

    if request.method == "POST" and request.user.has_perm('api.change_admin'):
        try:
            course = Course.objects.get(pk=content['course_id'])
            offering = Offering.objects.create(**content, course=course)
            offering.full_clean()
            offering.save()
            return JsonResponse({"response": offering.json_data(include_course_info=True)})
        except ValidationError as e:
            offering.delete()
            return JsonResponse({'error': e.message_dict})

    # NOTE No update because we dont want any editing of offering

    if request.method == "DELETE" and request.user.has_perm('api.change_admin'):
        try:
            course = Course.objects.get(pk=content['course_id'])
            offering = Offering.objects.get(course=course, offering_no=content['offering_no'])
            offering.delete()
            return JsonResponse({'response': str(offering.offering_no) + ' has been deleted.'})
        except Offering.DoesNotExist:
            return JsonResponse({"error": "Offering with #" + str(content['offering_no']) + " does not exist."})

    response = JsonResponse({'error': "Request not met."})
    response.status_code = 405
    return response


# 1
def prerequisite(request):
    try:
        content = json.loads(request.body)['content']
    except KeyError:
        return JsonResponse({"error": "Please wrap your request body with 'content' "})

    if request.method == "PUT" and request.user.has_perm('api.change_admin'):
        try:
            prereq = Course.objects.get(pk=content['prerequisite_id'])
            parent = Course.objects.get(pk=content['parent_id'])
        except Course.DoesNotExist:
            return JsonResponse({"error": "Your prerequisite or parent course does not exist."})
        setattr(prereq, "parent", parent)
        prereq.full_clean()
        prereq.save()
        return JsonResponse({'response': "success", 'content': parent.json_data(include_prerequisites=True)})

    if request.method == "DELETE" and request.user.has_perm('api.change_admin'):
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


# 2
def admin(request):
    try:
        content = json.loads(request.body)['content']
    except KeyError:
        return JsonResponse({"error": "Please wrap your request body with 'content' "})

    if request.method == "GET":
        person = Person.objects.get(pk=content['sin'])
        return JsonResponse({'response': "success", 'content': person.json_data()})

    if request.method == "POST":
        try:
            administrator = Admin.objects.create(**content)
            administrator.full_clean()
            administrator.save()

            content_type = ContentType.objects.get_for_model(Admin)
            content_type1 = ContentType.objects.get_for_model(Teacher)
            content_type2 = ContentType.objects.get_for_model(Counselor)
            content_type3 = ContentType.objects.get_for_model(Student)
            permission = Permission.objects.get(
                codename='change_admin',
                content_type=content_type,
            )
            permission1 = Permission.objects.get(
                codename='change_teacher',
                content_type=content_type1,
            )
            permission2 = Permission.objects.get(
                codename='change_counselor',
                content_type=content_type2,
            )
            permission3 = Permission.objects.get(
                codename='change_student',
                content_type=content_type3,
            )
            user = User.objects.create_user(username=content['sin'], password=content['password'])
            user.user_permissions.add(permission)
            user.user_permissions.add(permission1)
            user.user_permissions.add(permission2)
            user.user_permissions.add(permission3)

            return JsonResponse({"response": administrator.json_data()})
        except ValidationError as e:
            administrator.delete()
            return JsonResponse({'error': e.message_dict})

    if request.method == "PUT" and request.user.has_perm('api.change_admin'):
        try:
            administrator = Admin.objects.get(pk=content['sin'])
        except Admin.DoesNotExist:
            return JsonResponse({"error": "Admin with sin: " + str(content['sin']) + " does not exist."})
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

    if request.method == "DELETE" and request.user.has_perm('api.change_admin'):
        try:
            administrator = Admin.objects.get(pk=content['sin'])
            administrator.delete()
            User.objects.get(username=content['sin']).delete()
            return JsonResponse({'response': 'success'})
        except Admin.DoesNotExist:
            return JsonResponse({"error": "Admin with sin " + str(content['sin']) + " does not exist."})

    response = JsonResponse({'error': "Request not met."})
    response.status_code = 405
    return response


# 3
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

    if request.method == "POST" and request.user.has_perm('api.change_teacher'):
        try:
            course = Course.objects.get(pk=content['course_id'])
            offering = Offering.objects.get(course=course, offering_no=content['offering_no'])
            assignment = Assignment.objects.create(offering=offering, assign_no=content['assign_no'],
                                                   name=content['name'], description=content['description'])
            assignment.full_clean()
            assignment.save()
            return JsonResponse({"response": assignment.json_data()})
        except ValidationError as e:
            assignment.delete()
            return JsonResponse({'error': e.message_dict})

    if request.method == "PUT" and request.user.has_perm('api.change_teacher'):
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

    if request.method == "DELETE" and request.user.has_perm('api.change_teacher'):
        course = Course.objects.get(pk=content['course_id'])
        offering = Offering.objects.get(course=course, offering_no=content['offering_no'])
        assignment = Assignment.objects.get(offering=offering, assign_no=content['assign_no'])
        assignment.delete()
        return JsonResponse({'response': 'success'})

    response = JsonResponse({'error': "Request not met."})
    response.status_code = 405
    return response


# 4
def material(request):
    try:
        content = json.loads(request.body)['content']
    except KeyError:
        return JsonResponse({"error": "Please wrap your request body with 'content' "})

    course = Course.objects.get(pk=content['course_id'])
    offering = Offering.objects.get(course=course, offering_no=content['offering_no'])

    if request.method == "GET":
        material = Material.objects.get(offering=offering, material_no=content['material_no'])
        return JsonResponse({"response": material.json_data()})

    if request.method == "POST" and request.user.has_perm('api.change_teacher'):
        try:
            material = Material.objects.create(offering=offering, material_no=content['material_no'],
                                               name=content['name'], category=content['category'],
                                               description=content['description'])
            material.full_clean()
            material.save()
            return JsonResponse({"response": material.json_data()})
        except ValidationError as e:
            material.delete()
            return JsonResponse({'error': e.message_dict})

    if request.method == "PUT" and request.user.has_perm('api.change_teacher'):
        material = Material.objects.get(offering=offering, material_no=content['material_no'])

        try:
            for attr, value in content.items():
                setattr(material, attr, value)
            material.full_clean()
            material.save()
            return JsonResponse({'response': "success", 'content': material.json_data()})
        except ValidationError as e:
            return JsonResponse({'error': e.message_dict})

    if request.method == "DELETE" and request.user.has_perm('api.change_teacher'):
        material = Material.objects.get(offering=offering, material_no=content['material_no'])
        material.delete()
        return JsonResponse({'response': 'success'})

    response = JsonResponse({'error': "Request not met."})
    response.status_code = 405
    return response


# 1
def student_textbook(request):
    content = json.loads(request.body)['content']

    student = Student.objects.get(pk=content['sin'])
    textbook = Textbook.objects.get(isbn=content['isbn'], book_no=content['book_no'])

    if request.method == "POST" and request.user.has_perm('api.change_student'):
        textbook.student = student
        textbook.full_clean()
        textbook.save()
        return JsonResponse({'response': 'success', 'content': student.json_data()})

    if request.method == "DELETE" and request.user.has_perm('api.change_student'):
        textbook.student = None
        textbook.save()
        return JsonResponse({'response': 'Student textbook deleted.'})

    response = JsonResponse({"error": " Request not met."})
    response.status_code = 405
    return response


# 2
def student(request):
    content = json.loads(request.body)['content']

    if request.method == "GET":
        try:
            student1 = Student.objects.get(pk=content['sin'])
            return JsonResponse({"response": student1.json_data()})
        except Student.DoesNotExist:
            return JsonResponse({"error": "Student with SIN:" + str(content['sin']) + " does not exist."})

    if request.method == "PUT" and request.user.has_perm('api.change_admin'):
        student1 = Student.objects.get(pk=content['sin'])

        try:
            for attr, value in content.items():
                setattr(student1, attr, value)
            student1.full_clean()
            student1.save()
            return JsonResponse({'response': "success", 'content': student1.json_data()})
        except ValidationError as e:
            return JsonResponse({'error': e.message_dict})

    if request.method == "POST" and request.user.has_perm('api.change_admin'):
        try:
            student = Student.objects.create(**content)
            student.full_clean()
            student.save()

            content_type = ContentType.objects.get_for_model(Student)
            permission = Permission.objects.get(
                codename='change_student',
                content_type=content_type,
            )
            user = User.objects.create_user(username=content['sin'], password=content['password'])
            user.user_permissions.add(permission)

            return JsonResponse({"response": student.json_data()})
        except ValidationError as e:
            student.delete()
            return JsonResponse({'error': e.message_dict})

    if request.method == "DELETE" and request.user.has_perm('api.change_admin'):
        try:
            student1 = Student.objects.get(pk=content['sin'])
            student1.delete()
            User.objects.get(username=content['sin']).delete()
            return JsonResponse({"response": "success"})
        except Student.DoesNotExist:
            return JsonResponse({"error": "Student with SIN: " + str(content['sin']) + " does not exist."})

    response = JsonResponse({"error": "request not met."})
    response.status_code = 405
    return response


# 3
def textbook_author(request):
    content = json.loads(request.body)['content']

    if request.method == "POST" and request.user.has_perm('api.change_admin'):
        textbook = Textbook.objects.get(isbn=content['isbn'], book_no=content['book_no'])
        textbook_author = TextbookAuthor.objects.create(textbook=textbook, author=content['author'])
        textbook_author.full_clean()
        textbook_author.save()
        return JsonResponse({'response': 'Textbook_author created.'})

    if request.method == "DELETE" and request.user.has_perm('api.change_admin'):
        textbook = Textbook.objects.get(isbn=content['isbn'], book_no=content['book_no'])
        textbook_author = TextbookAuthor.objects.get(textbook=textbook, author=content['author'])
        textbook_author.textbook = None
        textbook_author.save()

    response = JsonResponse({"error": "Request not met."})
    response.status_code = 405
    return response


# 4
def textbook(request):
    inputInfo = json.loads(request.body)['content']

    if request.method == "GET":
        try:
            textbook1 = Textbook.objects.get(book_no=inputInfo['book_no'], isbn=inputInfo['isbn'])
            return JsonResponse({'response': "success", "content": textbook1.json_data()})
        except Textbook.DoesNotExist:
            return JsonResponse({"error": "Textbook with key:" + str(content['book_no']) +
                                          "," + str(content['isbn']) + " does not exist."})

    if request.method == "PUT" and request.user.has_perm('api.change_admin'):
        textbook1 = Textbook.objects.get(book_no=inputInfo['book_no'], isbn=inputInfo['isbn'])

        try:
            for attr, value in inputInfo.items():
                setattr(textbook1, attr, value)
            textbook1.full_clean()
            textbook1.save()
            return JsonResponse({'response': "success", 'content': textbook1.json_data()})
        except ValidationError as e:
            return JsonResponse({'error': e.message_dict})

    if request.method == "POST" and request.user.has_perm('api.change_admin'):
        try:
            textbook = Textbook.objects.create(**inputInfo)
            textbook.full_clean()
            textbook.save()
            return JsonResponse({"response": textbook.json_data()})
        except ValidationError as e:
            textbook.delete()
            return JsonResponse({'error': e.message_dict})
        except IntegrityError:
            return JsonResponse({'error': "Object could not be created."})

    if request.method == "DELETE" and request.user.has_perm('api.change_admin'):
        try:
            textbook1 = Textbook.objects.get(book_no=inputInfo['book_no'], isbn=inputInfo['isbn'])
            textbook1.delete()
            return JsonResponse({"response": "Success"})
        except Textbook.DoesNotExist:
            return JsonResponse({"error": "Textbook with key: " + str(content['book_no']) +
                                          "," + str(content['isbn']) + " does not exist."})

    response = JsonResponse({"error": "Request not met."})
    response.status_code = 405
    return response


# 1
def counselor(request):
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

    if request.method == "POST" and request.user.has_perm('api.change_admin'):
        try:
            counselor = Counselor.objects.create(**content)
            counselor.full_clean()
            counselor.save()

            content_type2 = ContentType.objects.get_for_model(Counselor)
            content_type3 = ContentType.objects.get_for_model(Student)
            permission2 = Permission.objects.get(
                codename='change_counselor',
                content_type=content_type2,
            )
            permission3 = Permission.objects.get(
                codename='change_student',
                content_type=content_type3,
            )
            user = User.objects.create_user(username=content['sin'], password=content['password'])
            user.user_permissions.add(permission2)
            user.user_permissions.add(permission3)

            return JsonResponse({"response": counselor.json_data()})
        except ValidationError as e:
            counselor.delete()
            return JsonResponse({'error': e.message_dict})
        except IntegrityError:
            return JsonResponse({'error': "Object could not be created."})

    if request.method == "PUT" and request.user.has_perm('api.change_admin'):
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

    if request.method == "DELETE" and request.user.has_perm('api.change_admin'):
        try:
            counselor = Counselor.objects.get(pk=content['sin'])
            counselor.delete()
            User.objects.get(username=content['sin']).delete()
            return JsonResponse({'response': str(counselor.name) + ' has been deleted.'})
        except Counselor.DoesNotExist:
            return JsonResponse({"error": "Counselor with sin " + str(content['sin']) + " does not exist."})

    response = JsonResponse({'error': "Request not met."})
    response.status_code = 405
    return response


# 2
def counselor_office_hours(request):
    try:
        content = json.loads(request.body)['content']
    except KeyError:
        return JsonResponse({"error": "Please wrap your request body with 'content' "})

    if request.method == "GET":
        try:
            office_hours = CounselorOfficeHour.objects.get(counselor_sin=content['counselor_sin'])
            return JsonResponse({'response': "success", 'content': office_hours.json_data()})
        except CounselorOfficeHour.DoesNotExist:
            return JsonResponse(
                {"error": "Counselor with sin " + str(content['counselor_sin']) + " does not have any office hours."})
        except KeyError:
            return JsonResponse({"error": "No sin included"})

    if request.method == "POST" and request.user.has_perm('api.change_counselor'):
        try:
            office_hours = CounselorOfficeHour.objects.create(**content)
            office_hours.full_clean()
            office_hours.save()
            return JsonResponse({"response": office_hours.json_data()})
        except ValidationError as e:
            office_hours.delete()
            return JsonResponse({'error': e.message_dict})
        except IntegrityError:
            return JsonResponse({'error': "Object could not be created."})

    if request.method == "PUT" and request.user.has_perm('api.change_counselor'):
        try:
            office_hours = CounselorOfficeHour.objects.get(counselor_sin=content['counselor_sin'])
        except CounselorOfficeHour.DoesNotExist:
            return JsonResponse({"error": "Counselor with sin " + str(content['counselor_sin']) + " does not exist."})
        except KeyError:
            return JsonResponse({"error": "No sin included"})

        try:
            for attr, value in content.items():
                setattr(office_hours, attr, value)
            office_hours.full_clean()
            office_hours.save()
            return JsonResponse({'response': "success", 'content': office_hours.json_data()})
        except ValidationError as e:
            return JsonResponse({'error': e.message_dict})

    if request.method == "DELETE" and request.user.has_perm('api.change_counselor'):
        try:
            office_hours = CounselorOfficeHour.objects.get(counselor_sin=content['counselor_sin'])
            office_hours.delete()
            return JsonResponse({'response': 'success'})
        except CounselorOfficeHour.DoesNotExist:
            return JsonResponse({"error": "Counselor with sin " + str(content['counselor_sin']) + " does not exist."})

    response = JsonResponse({'error': "Request not met."})
    response.status_code = 405
    return response


# 3
def counsels(request):
    try:
        content = json.loads(request.body)['content']
    except KeyError:
        return JsonResponse({"error": "Please wrap your request body with 'content' "})

    if request.method == "POST" and request.user.has_perm('api.change_counselor'):
        counselor = Counselor.objects.get(pk=content['counselor_sin'])
        student = Student.objects.get(pk=content['student_sin'])
        counselor.counsels.add(student)
        counselor.full_clean()
        counselor.save()
        return JsonResponse({'response': "success", 'content': counselor.json_data()})

    if request.method == "DELETE" and request.user.has_perm('api.change_counselor'):
        counselor = Counselor.objects.get(pk=content['counselor_sin'])
        student = Student.objects.get(pk=content['student_sin'])
        counselor.counsels.remove(student)
        counselor.save()
        return JsonResponse({'response': "success", 'content': counselor.json_data()})

    response = JsonResponse({'error': "Request not met."})
    response.status_code = 405
    return response


# 4
def room(request):
    try:
        content = json.loads(request.body)['content']
    except KeyError:
        return JsonResponse({"error": "Please wrap your request body with 'content' "})

    if request.method == "GET":
        room = Room.objects.get(pk=content['room_no'])
        return JsonResponse({"response": room.json_data()})

    if request.method == "POST" and request.user.has_perm('api.change_admin'):
        try:
            room = Room.objects.create(**content)
            room.full_clean()
            room.save()
            return JsonResponse({"response": room.json_data()})
        except ValidationError as e:
            room.delete()
            return JsonResponse({'error': e.message_dict})

    if request.method == "PUT" and request.user.has_perm('api.change_admin'):
        room = Room.objects.get(pk=content['room_no'])
        try:
            for attr, value in content.items():
                setattr(room, attr, value)
            room.full_clean()
            room.save()
            return JsonResponse({'response': "success", 'content': room.json_data()})
        except ValidationError as e:
            return JsonResponse({'error': e.message_dict})

    if request.method == "DELETE" and request.user.has_perm('api.change_admin'):
        room = Room.objects.get(pk=content['room_no'])
        room.delete()
        return JsonResponse({'response': 'success'})

    response = JsonResponse({'error': "Request not met."})
    response.status_code = 405
    return response


# 1
def schedule(request):
    content = json.loads(request.body)['content']

    course = Course.objects.get(pk=content['course_id'])
    offering = Offering.objects.get(course=course, offering_no=content['offering_no'])
    student = Student.objects.get(pk=content['sin'])

    if request.method == "GET":
        schedule = Schedule.objects.get(offering=offering, student=student)
        return JsonResponse(schedule.json_data())

    if request.method == "POST" and request.user.has_perm('api.change_student'):
        schedule = Schedule.objects.create(offering=offering, student=student, semester=content['semester'],
                                           grade=content['grade'])
        schedule.full_clean()
        schedule.save()
        return JsonResponse({"response": schedule.json_data()})

    if request.method == "PUT" and request.user.has_perm('api.change_student'):
        schedule = Schedule.objects.get(offering=offering, student=student)

        for attr, value in content.items():
            setattr(schedule, attr, value)
        schedule.full_clean()
        schedule.save()
        return JsonResponse({'response': "success", 'content': schedule.json_data()})

    if request.method == "DELETE" and request.user.has_perm('api.change_student'):
        schedule = Schedule.objects.get(offering=offering, student=student)
        schedule.delete()
        return JsonResponse({'response': 'success'})


def getAllCourses(request):
    return JsonResponse(
        {'response': list(map(lambda c: c.json_data(include_prerequisites=True), Course.objects.all()))})


def getAllStudents(request):
    return JsonResponse({'response': list(map(lambda s: s.json_data(), Student.objects.all()))})


def getAllTeachers(request):
    return JsonResponse({'response': list(map(lambda s: s.json_data(), Teacher.objects.all()))})


def getAllCounselors(request):
    return JsonResponse({'response': list(map(lambda s: s.json_data(), Counselor.objects.all()))})


def getAllAdmins(request):
    return JsonResponse({'response': list(map(lambda s: s.json_data(), Admin.objects.all()))})
