from django.shortcuts import render,get_object_or_404
from django.http import JsonResponse
from students.models import Student
from .serializers import StudentSerializer, EmployeeSerializer 
from rest_framework .response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from employee.models import Employee
from django.http import Http404
from rest_framework import mixins, generics, viewsets
from blogs.models import Blog,Comment
from blogs.serializers import BlogSerializer,CommentSerializer 
from.paginations import CustomPagination
from employee.filters import EmployeeFilter
from rest_framework.filters import SearchFilter,OrderingFilter

# ----------------------CRUD OPERATIONS BY FUNCTION BASED VIEW -------------------------------- 
# USE MANUALLY LIST FOR PRINT JSON DATA #
"""def studentsview(request):
    student = Student.objects.all()
    students = list(student.values())
    print(student)
    return JsonResponse(students ,safe=False)"""
    
# USE SERIALIZER FOR PRINT JSON DATA #
# SERIALIZER = CONVERT DATA IN TO JSON TO MODEL OR VISAVERSA LIKE LUNGAGE TRANSLATOR #
@api_view(['GET' , 'POST'])
def studentsview(request):
    if request.method =='GET':
        student = Student.objects.all()
        serializer = StudentSerializer(student, many = True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# GET PARTICULAR STUDENT INFO BY ID  #
@api_view(['GET' , 'PUT', 'DELETE'])
def studentdetails(request,pk):
    try: 
        student = Student.objects.get(pk=pk)
    except Student.DoesNotExit:
        return Response(status=status.HTTP_404_NOT_FOUND)   
    
    if request.method == 'GET':
        serializer = StudentSerializer(student)
        return Response(serializer.data,status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        serializer = StudentSerializer(student,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_404_NOT_FOUND)
    
    elif request.method == 'DELETE':
        student.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
"""# ----------------------CRUD OPERATIONS BY CLASSS BASED VIEW IN EMPLOYEE MODEL -------------------------------- 

class Employees(APIView):
    # get employee data 
    def get(self, request):
        employees = Employee.objects.all()
        serializer = EmployeeSerializer(employees,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    # post employee data     
    def post(self, request):
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)  
    
# show particular employee detail    
class EmployeesDetail(APIView):
    def get_object(self, pk):
        try:
            return Employee.objects.get(pk=pk)
        except Employee.DoseNotExit:
            raise Http404       
        
    def get(self,request,pk):
        employee = self.get_object(pk)
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data, status=status.HTTP_200_OK)          
    
    # modified detail 
    def put(self , request, pk):
        employee = self.get_object(pk)
        serializer = EmployeeSerializer(employee,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.error,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk):
        employee = self.get_object(pk)
        employee.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ----------------------CRUD OPERATIONS BY MIXINS CLASS (REUSABLE CODE) BASED VIEW IN EMPLOYEE MODEL -------------------------------- 
# MIXINS IS USED WITH GENERICS.GENERICSAPIVIEW (GENERICS IS GET STRUCTURE RESPONSE FROM HTTP E.G.: HTTP_201_OK)

class Employees(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    
    # SHOW EMPLOYEE LIST 
    def get(self,request):
        return self.list(request)   
    
    # CREATE EMPLOYEE 
    def post(self,request):
        return self.create(request)
    
class EmployeesDetail(mixins.RetrieveModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin,generics.GenericAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    
    # GET PARTICULAR EMPLOYEE 
    def get(self,request,pk):
        return self.retrieve(request,pk)
    
    # UPATE EMPLOYEE
    def put(self,request,pk):
        return self.update(request,pk)
    
    # DELETE EMPLOYEE
    def delete(self,request,pk):
        return self.destroy(request,pk)
    

# ----------------------CRUD OPERATIONS BY GENERIC CLASS BASED VIEW IN EMPLOYEE MODEL -------------------------------- 
# GENERICS ARE COMBINED 2 FUNCTION IN ONE 1 LKE LIST + CREATE . 3 FUNCTION IN 1 RETRIVE + UPDATE + DESTROY + 

class Employees(generics.ListCreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class EmployeesDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    lookup_field = 'pk' 
    

# VIEW SET COMBINED BOTH VIEWS 
#  TWO TYPE 
# 1] (VIEWSETS.VIEWSET : ALL FUNCTION APPLYED LIST,CREATE, UPDATE,RETRIVE,DESTROY)
# 2] (VIEWSETS.MODELVIEWSET : TAKE QUERYSET AND SERIALIZER CLASS AND AUTOMATICALLY PROVIDE BOTH PK AND NON PK BASED OPERATIONS )

# 1] VIEWSETS.VIEWSET
class EmployeeViewset(viewsets.ViewSet):
    def list(self,request):
        queryset = Employee.objects.all()
        serializer = EmployeeSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def create(self,request):
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors)
    
    def retrieve(self,request,pk=None):
        employee = get_object_or_404(Employee, pk=pk)
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def update(self,request,pk=None):
        employee = get_object_or_404(Employee, pk=pk)
        serializer = EmployeeSerializer(employee,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    def delete(self,request,pk=None):
        employee=get_object_or_404(Employee,pk=pk)
        employee.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
"""
    
# 2] (VIEWSETS.MODELVIEWSET    
    
class EmployeeViewset(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    #pagination_class = CustomPagination
    filterset_class = EmployeeFilter
    #filterset_fields = ['emp_designation']
    

    
# NESTED SERIALIZER  ITS GIVE DATA WITH RELATED (USIG FOREGN KEY )
    
class BlogsView(generics.ListCreateAPIView):
        queryset = Blog.objects.all()
        serializer_class = BlogSerializer
        # THIS CODE NOT WORKED 
        filter_backends = [SearchFilter, OrderingFilter]
        search_fields = ['blog_title', 'blog_body']
        ordering_fields = ['id']
        
        
class CommentsView(generics.ListCreateAPIView):
        queryset = Comment.objects.all()
        serializer_class = CommentSerializer
        
        
# PARTICULAR COMMENT AND BLOGS  
       
class BlogsDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    lookup_field ='pk'
    
    
            
class CommentsDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    lookup_field ='pk'