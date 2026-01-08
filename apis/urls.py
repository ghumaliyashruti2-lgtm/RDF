from django.urls import path,include
from .import views 
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('employees',views.EmployeeViewset, basename='employee')

urlpatterns = [
    path('students/',views.studentsview),
    path('students/<int:pk>/',views.studentdetails),
    path('',include(router.urls)),
]
