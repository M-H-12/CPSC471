from django.db import models
from polymorphic.models import PolymorphicModel


class Person(PolymorphicModel):
    sin = models.PositiveIntegerField(primary_key=True)  # FIXME Restrict to only being 9 in length
    name = models.CharField(max_length=255)
    gender = models.CharField(max_length=1)
    id = models.PositiveIntegerField(unique=True)
    password = models.CharField(max_length=50)

    def json_data(self, **kwargs):
        person = {
            'sin': self.sin,
            'name': self.name,
            'gender': self.gender,
            'id': self.id,
            'password': self.password
        }
        return person


class Course(models.Model):
    course_id = models.PositiveIntegerField(primary_key=True)
    course_name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', related_name='prerequisites',
                               on_delete=models.SET_NULL, blank=True, null=True)

    def json_data(self, include_prerequisites=False, **kwargs):
        course = {
            'course_id': self.course_id,
            'course_name': self.course_name,
            'offerings': list(map(lambda offering: offering.json_data(include_course_info=False, include_room=True),
                                  self.offerings.all())),
            'required_textbooks': list(map(lambda textbook: textbook.json_data(True), self.required_textbooks.all()))
        }
        if include_prerequisites:
            course['prerequisites'] = list(map(lambda prereq: prereq.json_data(False), self.prerequisites.all()))
        return course


class Student(Person):
    year = models.PositiveSmallIntegerField()
    grade_average = models.FloatField()
    credits_received = models.PositiveIntegerField()

    def json_data(self, **kwargs):
        students = {
            'year': self.year,
            'grade_average': self.grade_average,
            'credits_received': self.credits_received,
            'signed_out_textbooks': list(map(lambda textbook: textbook.json_data(True), self.signed_out_textbooks.all()))
        }
        json_data = super().json_data()
        json_data.update(students)
        return json_data


class Counselor(Person):
    counsels = models.ManyToManyField(Student, blank=True)
    salary = models.FloatField()
    hired_year = models.PositiveIntegerField(editable=False)
    hired_date = models.PositiveIntegerField(editable=False)
    hired_month = models.CharField(editable=False, max_length=9, blank=False)

    def json_data(self, **kwargs):
        counselor = {
            'salary': self.salary,
            'hired_date': str(self.hired_year) + "-" + self.hired_month + "-" + str(self.hired_date),
            'counsels': list(map(lambda student: student.json_data(True), self.counsels.all())),
            'office_hours': list(map(lambda office_hour: office_hour.json_data(True),
                                     self.officehours.all()))
        }
        json_data = super().json_data()
        json_data.update(counselor)
        return json_data


class CounselorOfficeHour(models.Model):
    counselor = models.ForeignKey(Counselor, related_name='officehours', on_delete=models.CASCADE)
    day = models.CharField(max_length=9)
    hour_from = models.PositiveSmallIntegerField()  # TODO Make sure hour_from and hour_to are <= 23
    hour_to = models.PositiveSmallIntegerField()

    def json_data(self, **kwargs):
        json_data = {
            'day': self.day,
            'hour_from': self.hour_from,
            'hour_to': self.hour_to
        }
        return json_data


class Teacher(Person):
    can_teach = models.ManyToManyField(Course, blank=True)
    salary = models.FloatField()
    hired_year = models.PositiveIntegerField(editable=False)
    hired_date = models.PositiveIntegerField(editable=False)
    hired_month = models.CharField(editable=False, max_length=9, blank=False)

    def json_data(self, **kwargs):
        teacher = {
            'salary': self.salary,
            'hired_date': str(self.hired_year) + "-" + self.hired_month + "-" + str(self.hired_date),
            'can_teach': list(map(lambda course: course.json_data(False), self.can_teach.all())),
            'office_hours': list(map(lambda hours: hours.json_data(True), self.officehours.all()))
        }
        json_data = super().json_data()
        json_data.update(teacher)
        return json_data


class TeacherOfficeHour(models.Model):
    teacher = models.ForeignKey(Teacher, related_name='officehours', on_delete=models.CASCADE)
    day = models.CharField(max_length=9)
    hour_from = models.PositiveSmallIntegerField()  # TODO Make sure hour_from and hour_to are <= 23
    hour_to = models.PositiveSmallIntegerField()

    def json_data(self, **kwargs):
        json_data = {
            'day': self.day,
            'hour_from': self.hour_from,
            'hour_to': self.hour_to
        }
        return json_data


class Room(models.Model):
    room_no = models.PositiveIntegerField(primary_key=True)
    max_capacity = models.PositiveIntegerField()  # TODO Set maximum

    def json_data(self):
        room = {
            'room_no': self.room_no,
            'max_capacity': self.max_capacity,
            'schedule': list(map(lambda timeslot: timeslot.json_data(include_course_info=True, include_room=False),
                                 self.timeslots.all()))
        }
        return room


class Offering(models.Model):
    course = models.ForeignKey(Course, related_name='offerings', on_delete=models.CASCADE)
    offering_no = models.PositiveIntegerField()
    no_of_students = models.PositiveIntegerField()
    room = models.ForeignKey(Room, related_name="timeslots", on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        unique_together = ('course', 'offering_no',)

    def json_data(self, include_course_info=False, include_room=False, **kwargs):
        offering = {
            'offering_no': self.offering_no,
            'no_of_students': self.no_of_students,
            'times': list(map(lambda time: time.json_data(True), self.times.all()))
        }
        if include_course_info:
            offering['course_id'] = self.course.course_name
        if self.room and include_room:
            offering['room_no'] = self.room.room_no
        return offering


class OfferingDayAndTime(models.Model):
    offering = models.ForeignKey(Offering, related_name='times', on_delete=models.CASCADE)
    day = models.CharField(max_length=9)
    hour_from = models.PositiveSmallIntegerField()  # TODO Make sure hour_from and hour_to are <= 23
    hour_to = models.PositiveSmallIntegerField()

    def json_data(self, **kwargs):
        offering_day_and_time = {
            'day': self.day,
            'hour_from': self.hour_from,
            'hour_to': self.hour_to
        }
        return offering_day_and_time


class Admin(Person):
    position_title = models.CharField(max_length=255)
    salary = models.FloatField()
    hired_year = models.PositiveIntegerField(editable=False)
    hired_date = models.PositiveIntegerField(editable=False)
    hired_month = models.CharField(editable=False, max_length=9, blank=False)

    def json_data(self, **kwargs):
        teacher = {
            'salary': self.salary,
            'hired_date': str(self.hired_year) + "-" + self.hired_month + "-" + str(self.hired_date),
            'position_title': self.position_title
        }
        json_data = super().json_data()
        json_data.update(teacher)
        return json_data


class Textbook(models.Model):
    isbn = models.IntegerField(primary_key=True)  # TODO Set length to 10
    book_no = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=255)
    year = models.IntegerField()  # TODO Set length to 4
    edition = models.IntegerField()
    course = models.ForeignKey(Course, related_name='required_textbooks', on_delete=models.SET_NULL, blank=True,
                               null=True)
    student = models.ForeignKey(Student, related_name='signed_out_textbooks', on_delete=models.SET_NULL, blank=True,
                                null=True)

    class Meta:
        unique_together = ('isbn', 'book_no',)

    def json_data(self):
        textbook = {
            'isbn': self.isbn,
            'book_no': self.book_no,
            'title': self.title,
            'year': self.year,
            'edition': self.edition,
            'authors': list(map(lambda author: author.get_author(), self.authors.all()))
        }
        return textbook


class TextbookAuthor(models.Model):
    textbook = models.ForeignKey(Textbook, related_name='authors', on_delete=models.CASCADE)
    author = models.CharField(max_length=255)

    def get_author(self):
        return self.author


class Material(models.Model):
    offering = models.ForeignKey(Offering, on_delete=models.CASCADE, editable=False)
    material_no = models.PositiveIntegerField(editable=False)
    name = models.CharField(max_length=255)
    upload_date = models.DateField(auto_now_add=True, editable=False)
    category = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('offering', 'material_no',)

    def json_data(self):
        material = {
            'material_no': self.material_no,
            'name': self.name.__str__(),
            'upload_date': self.upload_date.__str__(),
            'category': self.category,
            'description': self.description
        }
        return material


class Assignment(models.Model):
    offering = models.ForeignKey(Offering, on_delete=models.CASCADE, editable=False)
    assign_no = models.PositiveIntegerField(editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('offering', 'assign_no',)

    def json_data(self, **kwargs):
        assignment = {
            'assign_no': self.assign_no,
            'name': self.name,
            'description': self.description,
        }
        return assignment


class Schedule(models.Model):
    offering = models.ForeignKey(Offering, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    semester = models.CharField(max_length=255)
    grade = models.CharField(max_length=2, blank=True, null=True)

    class Meta:
        unique_together = ('offering', 'student',)

    def json_data(self, **kwargs):
        schedule = {
            'semester': self.semester,
            'grade': self.grade
        }
        json_data = self.offering.json_data(include_course_info=True, include_room=False)
        json_data.update(schedule)
        return json_data


