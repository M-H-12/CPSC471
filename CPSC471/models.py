from django.db import models


class Counselor(Staff):
    counsels = models.ManyToManyField(Student)

    def get_students(self):
        return self.counsels.all()

    def json_data(self):
        counselor = {
            'availability': list(map(lambda time: time, self.counseloravailability_set.all())),
            'students': list(map(lambda student: student.jsonData(True), self.getStudents()))
        }
        json_data = super().json_data()
        json_data.update(counselor)
        return json_data


class CounselorAvailability(models.Model):
    counselor = models.ForeignKey(Counselor)
    time = models.DateTimeField()  # FIXME Decide on whether to change to models.CharField()

    def json_data(self):
        times = {
            'time': self.time.__str__()
        }
        return times
