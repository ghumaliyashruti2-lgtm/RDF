from django.shortcuts import render 
from django.http import HttpResponse

# Create your views here.
def students(reqest):
    student = [
        {'id' : 1, 'name': 'shruti', 'age':20}
    ]
    return HttpResponse(student)