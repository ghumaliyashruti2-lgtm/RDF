from django.urls import path,include
from .import views 
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('employees',views.EmployeeViewset, basename='employee')

urlpatterns = [
    path('students/',views.studentsview),
    path('students/<int:pk>/',views.studentdetails),
    path('',include(router.urls)),
    
    path ('blogs/',views.BlogsView.as_view()),
    path ('comments/',views.CommentsView.as_view()),
    
    path ('blogs/<int:pk>/',views.BlogsDetailView.as_view()),
    path ('comments/<int:pk>/',views.CommentsDetailView.as_view()),
]
