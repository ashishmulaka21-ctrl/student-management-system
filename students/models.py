from django.db import models


class Student(models.Model):
    student_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    age = models.IntegerField()
    course = models.CharField(max_length=100)
    gender = models.CharField(max_length=20)
    address = models.TextField()

    def __str__(self):
        return self.name