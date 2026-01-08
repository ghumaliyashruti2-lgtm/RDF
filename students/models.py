from django.db import models

# Create your models here.
class Student(models.Model):
    student_name = models.CharField(max_length=30, blank=True, null=True)
    student_dpt =models.CharField(max_length=20, blank=True, null=True)
    
    def __str__(self):
        return self.student_name
