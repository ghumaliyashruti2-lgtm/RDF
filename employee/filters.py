import django_filters
from .models import Employee


class EmployeeFilter(django_filters.FilterSet):
    emp_designation = django_filters.CharFilter(field_name='emp_designation',lookup_expr='iexact')
    emp_name = django_filters.CharFilter(field_name='emp_name',lookup_expr='icontains')
    id = django_filters.RangeFilter(field_name='id')
    
    class Meta:
        model = Employee
        fields  = ['emp_designation','emp_name']
    
    """
    #THIS IS USED WHEN USER HAVE ENTER ANOTHER ID FIELD LIKE EMP_ID THIS IS NOT PK .
    min_id = django_filters.CharFilter(method='filter_by_id_range', label = 'From Emp Id')
    max_id = django_filters.CharFilter(method='filter_by_id_range', label = 'To Emp Id')
    
     class Meta:
        model = Employee
        fields  = ['emp_designation','emp_name','min_id', 'max_id']
    
    #THIS IS USED WHEN USER HAVE ENTER ANOTHER ID FIELD LIKE EMP_ID THIS IS NOT PK .def filter_by_id_range(self,queryset,name,value):
        if name == 'id_min':
            return queryset.filter(emp_id_gte=value)
        elif name == 'id_max':
            return queryset.filter(emp_id_lte=value)
        return queryset """