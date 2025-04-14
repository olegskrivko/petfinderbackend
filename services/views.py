# from django.shortcuts import render

# # Create your views here.
# # services/views.py
# from rest_framework import viewsets
# from .models import Service
# from .serializers import ServiceSerializer
# from rest_framework.permissions import IsAuthenticated

# class ServiceViewSet(viewsets.ModelViewSet):
#     queryset = Service.objects.all()
#     serializer_class = ServiceSerializer


# class ServiceViewSet(viewsets.ModelViewSet):
#     queryset = Service.objects.all()
#     serializer_class = ServiceSerializer
#     permission_classes = [IsAuthenticated]


# services/views.py
from rest_framework import viewsets, generics
from django_filters.rest_framework import DjangoFilterBackend
from .models import Service
from .serializers import ServiceSerializer
from .filters import ServiceFilter

class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ServiceFilter



class ServiceDetailView(generics.RetrieveAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    lookup_field = 'id'