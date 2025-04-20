
# services/views.py
from rest_framework import serializers
from rest_framework import viewsets, generics
from django_filters.rest_framework import DjangoFilterBackend
from .models import Service, WorkingHour, Location, Review
from .serializers import ServiceSerializer, ReviewSerializer
# from .filters import ServiceFilter
# Add this at the top if you haven't already
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import generics
from rest_framework.exceptions import ValidationError
from django_filters import rest_framework as filters


import django_filters
from django.db.models import Q
from django.contrib.auth import get_user_model
User = get_user_model()

class ServicePagination(PageNumberPagination):
    page_size = 6
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'totalPages': self.page.paginator.num_pages,
            'currentPage': self.page.number,
            'results': data
        })

# class ServiceFilter(django_filters.FilterSet):
class ServiceFilter(filters.FilterSet):
    # category = django_filters.CharFilter(field_name='category', lookup_expr='iexact')
    category = filters.NumberFilter(field_name='category', lookup_expr='exact')
    search = filters.CharFilter(method='filter_by_search', label='Search')
    # search = django_filters.CharFilter(method='filter_search')

    # def filter_search(self, queryset, name, value):
    #     return queryset.filter(
    #         Q(title__icontains=value) | Q(description__icontains=value)
    #     )
    def filter_by_search(self, queryset, name, value):
        """Split the search string into separate terms. Allow searching on title and description"""
        terms = value.strip().split()
        for term in terms:
            queryset = queryset.filter(
                Q(description__icontains=term) | Q(title__icontains=term)
            )
        return queryset

    class Meta:
        model = Service
        fields = ['search', 'category']

class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all().order_by('-created_at') # Order by created_at in descending order (most recent first)
    serializer_class = ServiceSerializer
    permission_classes = [IsAuthenticatedOrReadOnly] # Allow public read access, but auth required for write operations
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ServiceFilter
    pagination_class = ServicePagination

    #search_fields = ['title', 'description', 'location__address']  # example searchable fields

    parser_classes = (MultiPartParser, FormParser)
    def get_queryset(self):
        return super().get_queryset()
    
    def list(self, request, *args, **kwargs):
        # The pagination logic is handled automatically by the pagination class
        return super().list(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# class ServiceViewSet(viewsets.ModelViewSet):
#     queryset = Service.objects.all()
#     serializer_class = ServiceSerializer
#     filter_backends = (DjangoFilterBackend,)
#     filterset_class = ServiceFilter

#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)

class ServiceDetailView(generics.RetrieveAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    lookup_field = 'id'


class ReviewListCreateView(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        service_id = self.kwargs['service_id']
        return Review.objects.filter(service_id=service_id)

    # def perform_create(self, serializer):
    #     user = self.request.user
    #     service_id = self.kwargs['service_id']  # Get service_id from URL
    #     service = Service.objects.get(id=service_id)
        
    #     # Try to get the existing review, if any
    #     review, created = Review.objects.get_or_create(service=service, user=user)
        
    #     # If it's not a new review, update it
    #     if not created:
    #         review.rating = serializer.validated_data.get('rating', review.rating)
    #         review.comment = serializer.validated_data.get('comment', review.comment)
    #         review.save()
    #     else:
    #         # If it's a new review, save it
    #         review = serializer.save(user=user, service=service)
    def perform_create(self, serializer):
        user = self.request.user
        service_id = self.kwargs['service_id']
        service = Service.objects.get(id=service_id)

        # Check if the review already exists
        existing_review = Review.objects.filter(user=user, service=service).first()

        if existing_review:
            # Update existing review with validated data
            existing_review.rating = serializer.validated_data['rating']
            existing_review.comment = serializer.validated_data['comment']
            existing_review.save()
        else:
            # Create a new review using serializer (which already has validated data)
            serializer.save(user=user, service=service)



