
# services/views.py
from rest_framework import serializers
from rest_framework import viewsets, generics
from django_filters.rest_framework import DjangoFilterBackend
from .models import Service, WorkingHour, Location
from .serializers import ServiceSerializer
from .filters import ServiceFilter


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ServiceFilter

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ServiceDetailView(generics.RetrieveAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    lookup_field = 'id'


