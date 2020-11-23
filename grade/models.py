from django.db import models

# Create your models here.


class Grade(models.Model):

    name = models.CharField(max_length=16)

    def __str__(self):
        return self.name


class Subject(models.Model):
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE)
    name = models.CharField(max_length=32)

    def __str__(self):
        return f"{self.name} {self.grade.name}"
