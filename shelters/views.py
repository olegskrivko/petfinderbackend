from rest_framework import viewsets
from .models import Shelter
from .serializers import ShelterSerializer

class ShelterViewSet(viewsets.ModelViewSet):
    # Queryset to get all shelters, including any related data like sighting history
    queryset = Shelter.objects.all()  # Adjust the related fields as needed
    serializer_class = ShelterSerializer
    # permission_classes = [IsAuthenticated]  # Uncomment if you want authentication

