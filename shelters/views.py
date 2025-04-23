from rest_framework import viewsets
from .models import Shelter
from .serializers import ShelterSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class ShelterViewSet(viewsets.ModelViewSet):
    queryset = Shelter.objects.all()
    serializer_class = ShelterSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


