from django.db import models

class Employee(models.Model):
    emp_name = models.CharField(max_length=30, blank=True, null=True)
    emp_designation = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return self.emp_name