from django.db import models
from polymorphic.models import PolymorphicModel

class Staff(PolymorphicModel):
    SIN = models.IntegerField(primary_key=True)
    salary = models.IntegerField()
    hired_date = models.DateField()

    def json_data(self, **kwargs):
        staff = {
            'SIN': self.SIN,
            'salary': self.salary,
            'hired_date': self.hired_date
        }
        return staff

class Counselor(Staff):
    counsels = models.ManyToManyField(Student, blank=True)

    def json_data(self):
        counselor = {
            'counsels': list(map(lambda student: student.json_data(True), self.counsels.all())),
            'office_hours': list(map(lambda office_hour: office_hour.json_data(True),
                                     self.counselorofficehour_set.all()))
        }
        json_data = super().json_data()
        json_data.update(counselor)
        return json_data


class CounselorOfficeHour(models.Model):
    counselor = models.ForeignKey(Counselor, on_delete=models.CASCADE)
    day = models.CharField(max_length=9)
    hour_from = models.PositiveSmallIntegerField()
    hour_to = models.PositiveSmallIntegerField()

    def json_data(self):
        json_data = {
            'day': self.day,
            'hour_from': self.hour_from,
            'hour_to': self.hour_to
        }
        return json_data


class Teacher(Staff):
    can_teach = models.ManyToManyField(Course, blank=True)

    def json_data(self):
        teacher = {
            'can_teach': list(map(lambda course: course.json_data(True), self.can_teach.all())),
            'office_hours': list(map(lambda hours: hours.json_data(True), self.teacherofficehour_set.all()))
        }
        json_data = super().json_data()
        json_data.update(teacher)
        return json_data


class TeacherOfficeHour(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    day = models.CharField(max_length=9)
    hour_from = models.PositiveSmallIntegerField()
    hour_to = models.PositiveSmallIntegerField()

    def json_data(self):
        hours = {
            'day': self.day,
            'hour_from': self.hour_from,
            'hour_to': self.hour_to
        }
        return hours


class Room(models.Model):
    room_no = models.IntegerField()  # TODO Determine if blank=false
    max_capacity = models.IntegerField()  # TODO Determine if blank=false

    def json_data(self):
        room = {
            'room_no': self.room_no,
            'max_capacity': self.max_capacity
            #  'schedule': list(map(lambda timeslot: timeslot.json_data(True), self.offering_set.all()))
        }
        return room


class Material(models.Model):
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    offering_no = models.ForeignKey(Offering, on_delete=models.CASCADE)
    material_no = models.IntegerField()
    name = models.CharField()
    upload_date = models.DateTimeField(auto_now_add=True)
    category = models.CharField()
    description = models.CharField(blank=True)

    def json_data(self):
        material = {
            'material_no': self.material_no,
            'name': self.name.__str__(),
            'upload_date': self.upload_date,
            'category': self.category.__str__(),
            'description': self.description.__str__()
        }
        return material

class Course(models.Model):
    course_id = models.IntegerField(primary_key=True)
    course_name = models.CharField(max_length=20)
    Prerequisite = models.ForeignKey('self', related_name='course', on_delete=models.CASCADE)

    def json_data(self, **kwargs):
        course = {
            'course_id': self.course_id,
            'course_name': self.course_name.__str__
        }
        return course

class Offering(models.Model):
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    offering_no = models.IntegerField()
    no_of_students = models.IntegerField()
    room_no = models.IntegerField()

    def json_data(self, **kwargs):
        offering = {
            'course_id': self.course_id,
            'offering_no': self.offering_no,
            'no_of_students': self.no_of_students,
            'room_no': self.room_no
        }
        return offering

class Offering_day_and_time(models.Model):
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    offering_no = models.IntegerField()
    day = models.CharField()
    time = models.CharField()

    def json_data(self, **kwargs):
        offering_day_and_time = {
            'course_id': self.course_id,
            'offering_no': self.offering_no,
            'day': self.day.__str__,
            'time':self.time.__str__
        }
        return offering_day_and_time
