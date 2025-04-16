# services/filters.py
# import django_filters
# from .models import Service

# class ServiceFilter(django_filters.FilterSet):
#     category = django_filters.CharFilter(field_name='category', lookup_expr='icontains')
#     title = django_filters.CharFilter(field_name='title', lookup_expr='icontains')

#     class Meta:
#         model = Service
#         fields = ['category', 'title']

# services/filters.py
import django_filters
from .models import Service

class ServiceFilter(django_filters.FilterSet):
    category = django_filters.NumberFilter(field_name="category")

    class Meta:
        model = Service
        fields = ['category']
