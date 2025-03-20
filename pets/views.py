from django.shortcuts import render
from rest_framework.pagination import PageNumberPagination
# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Pet, PetSightingHistory
from .serializers import PetSerializer, PetSightingHistorySerializer
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import AllowAny
#from rest_framework.permissions import IsAuthenticated
from django_filters import rest_framework as filters
from django.db.models import OuterRef, Subquery
from django.db.models import Q
from django.utils.timezone import make_aware
from datetime import datetime
from django.utils import timezone
import django_filters
from django.utils.dateparse import parse_datetime
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.contrib.auth.models import User
from decimal import Decimal, InvalidOperation
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from rest_framework.permissions import BasePermission
from decimal import Decimal
from django.utils.timezone import now
from rest_framework.parsers import MultiPartParser, FormParser

class PetFilter(filters.FilterSet):
    species = filters.NumberFilter(field_name='species', lookup_expr='exact')
    age = filters.NumberFilter(field_name='age', lookup_expr='exact')  # Filter for age (exact match)
    gender = filters.NumberFilter(field_name='gender', lookup_expr='exact')  # Filter for gender
    size = filters.NumberFilter(field_name='size', lookup_expr='exact')  # Filter for size
    pattern = filters.NumberFilter(field_name='pattern', lookup_expr='exact')  # Filter for size
    # age_min = filters.NumberFilter(field_name='age', lookup_expr='gte')  # Minimum age filter
    # age_max = filters.NumberFilter(field_name='age', lookup_expr='lte')  # Maximum age filter
    # date = filters.DateFilter(method='filter_by_date')  # URL parameter "date"
    #date = django_filters.DateFilter(method='filter_by_date')  # Filter by date (specific event date)
        # Filter for created_at (creation date of the pet)
    #created_at = django_filters.DateFilter(method='filter_by_created_at')
    # Filter for created_at field, but expect the URL query param 'date'
    #date = django_filters.DateFilter(field_name='created_at', lookup_expr='exact', label="Created At")
   # Filter for created_at field using DateFilter
    #date = filters.DateFilter(field_name='created_at', lookup_expr='date', label="Created At")
    # Map the 'date' parameter to the 'timestamp' field with greater than or equal filter
    #date = filters.DateFilter(field_name='created_at', lookup_expr='gte', label="Date")
    #date = filters.IsoDateTimeFilter(field_name='created_at', lookup_expr='gte', label="Filter Pets by Creation Date")
    date = filters.IsoDateTimeFilter(method='filter_by_event_date', label="Filter by Event Date")
    # Filter for first status in PetSightingHistory
    status = filters.NumberFilter(method='filter_by_status')
    # Allow searching on name and notes
    search_fields = ['name', 'notes']  # Fields you want to allow search on
        # Add a filter for color 7 7 9 9 8 7
    color = filters.NumberFilter(method='filter_by_color')
    # date_str = '2025-01-01T00:00:00.000Z'
    # parsed_date = parse_datetime(date_str)
    # print(parsed_date)

    def filter_by_color(self, queryset, name, value):
        # Filter pets by either primary_color or secondary_color matching the selected color
        return queryset.filter(
            Q(primary_color=value) | Q(secondary_color=value)
        )
    
    # Custom filter for event date
    def filter_by_event_date(self, queryset, name, value):
        # Subquery to filter pets based on event_occurred_at from PetSightingHistory
        pets_with_event_date = PetSightingHistory.objects.filter(
            pet=OuterRef('pk'),
            event_occurred_at__gte=value
        ).values('pet')

        return queryset.filter(pk__in=Subquery(pets_with_event_date))
    

    def filter_by_status(self, queryset, name, value):
        # First, get the first status based on the timestamp for each pet
        first_status = PetSightingHistory.objects.filter(
            pet=OuterRef('pk')
        ).order_by('timestamp').values('status')  # No slicing yet

        # Now filter by the desired status
        first_status_filtered = first_status.filter(status=value)

        # Apply the Subquery filter to return pets with the matching first status
        return queryset.filter(
            pk__in=Subquery(first_status_filtered.values('pet'))  # Slice after filtering
            #pk__in=Subquery(first_status_filtered.values('pet'))  # ✅ Remove `[:1]`
        )


    class Meta:
        model = Pet
        fields = ['species', 'age', 'gender', 'size', 'status', 'pattern', 'color']

@api_view(['GET'])
@permission_classes([IsAuthenticated])  # Ensure only authenticated users can access
def get_user_pets(request):
    """
    Fetch all pets created by the logged-in user.
    """
    print(request)
    user = request.user  # Get the logged-in user
    print(request)
    pets = Pet.objects.filter(author=user)
    serializer = PetSerializer(pets, many=True)
    return Response(serializer.data)

# ✅ Custom permission: Only pet owners can edit/delete
class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Read-only permissions for everyone
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        # Write permissions only for the pet owner
        return obj.author == request.user
# Custom pagination class to include metadata in the response
class PetPagination(PageNumberPagination):
    page_size = 6  # Default page size
    page_size_query_param = 'page_size'  # Allow clients to set the page size
    max_page_size = 100  # Max number of items per page
    # You can override the `get_paginated_response` method if you want to customize the structure of the response.
    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,  # Total number of pets
            'totalPages': self.page.paginator.num_pages,  # Total pages
            'currentPage': self.page.number,  # Current page number
            'results': data  # The paginated results
        })


class PetViewSet(viewsets.ModelViewSet):
    #queryset = Pet.objects.all()
    queryset = Pet.objects.all().prefetch_related('sightings_history').order_by('id')  # Optimized query to prefetch related sighting data
    serializer_class = PetSerializer
    pagination_class = PetPagination  # Set the custom pagination class here
    parser_classes = (MultiPartParser, FormParser)  # ✅ Handle file uploads
    #permission_classes = [IsAuthenticated]  # Only authenticated users can modify pets
    #permission_classes = [AllowAny]
    permission_classes = [IsAuthenticated]  # Restrict creation to authenticated users only
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_class = PetFilter  # Ensure this is used for filtering
    # Add search_fields here directly for search functionality
    search_fields = ['name', 'notes']  # Fields you want to allow search on
    #ordering_fields = ['name', 'age']  # Optional: Fields that can be used for ordering

    def get_queryset(self):
        queryset = super().get_queryset()

        # Retrieve the search term from the query parameters
        search = self.request.query_params.get('search', None)
        
        if search:
            # Search for pets by name and notes fields
            queryset = queryset.filter(
                Q(name__icontains=search) | Q(notes__icontains=search)
            )
        
        # Apply the filters from PetFilter if any are present in the request
        return queryset
    
    def list(self, request, *args, **kwargs):
        print("Query Params:", request.query_params)
        queryset = self.get_queryset()
        print("Filtered Queryset:", queryset)
        return super().list(request, *args, **kwargs)
    
    # def perform_create(self, serializer):
    #     """
    #     Save the pet with its author and ensure a PetSightingHistory entry is created.
    #     """
    #     print("hello from perform_create", serializer)
    #     # Assign the logged-in user as the author
    #     serializer.save(author=self.request.user)
    def perform_create(self, serializer):
        print("hello from perform_create", serializer)
        """ ✅ Create a new Pet and its first PetSightingHistory automatically (Fix) """
        # Save the Pet instance first
        pet = serializer.save(author=self.request.user) # Save pet and assign author
        # Save Pet instance (author is assigned inside serializer)
        #pet = serializer.save()
        

        # Retrieve latitude, longitude, and status from the request data
        latitude = self.request.data.get("latitude")
        longitude = self.request.data.get("longitude")
        status = self.request.data.get("status")
        event_occurred_at = self.request.data.get("date") + " " + self.request.data.get("time")  # Combine date & time

        # Validate required fields
        if not latitude or not longitude or not status:
            return Response(
                {"error": "Latitude, longitude, and status are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Convert latitude and longitude to Decimal for database storage
            latitude = Decimal(latitude)
            longitude = Decimal(longitude)
        except (ValueError, TypeError):
            return Response(
                {"error": "Invalid latitude or longitude format"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Ensure the status is a valid integer
        try:
            status = int(status)
            if status not in dict(PetSightingHistory.STATUS_CHOICES):
                return Response({"error": "Invalid status value"}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError:
            return Response({"error": "Invalid status format"}, status=status.HTTP_400_BAD_REQUEST)

        # Convert event_occurred_at to a valid datetime
        try:
            event_occurred_at = datetime.strptime(event_occurred_at, "%Y-%m-%d %H:%M")
        except ValueError:
            event_occurred_at = now()  # Fallback to current timestamp if invalid

        # Create the first sighting record
        PetSightingHistory.objects.create(
            pet=pet,
            status=status,
            latitude=latitude,
            longitude=longitude,
            event_occurred_at=event_occurred_at,
            reporter=self.request.user  # Set the user who created the pet as the first reporter
        )

        print("✅ PetSightingHistory created successfully for pet:", pet.id)
    
    def retrieve(self, request, pk=None):
        """ ✅ Allow all users to retrieve pets """
        pet = get_object_or_404(Pet, pk=pk)  # Remove `author=request.user`
        serializer = self.get_serializer(pet)
        return Response(serializer.data)
    # def retrieve(self, request, pk=None):
    #     """
    #     Retrieve a specific pet by ID.
    #     """
    #     print("retrieve")
    #     pet = get_object_or_404(Pet, pk=pk, author=request.user)
    #     print("pet", pet)
    #     serializer = self.get_serializer(pet)
    #     print("serializer", serializer)
    #     return Response(serializer.data)
    
    def update(self, request, pk=None):
        """
        Update pet details.
        """
        print("update")
        pet = get_object_or_404(Pet, pk=pk, author=request.user)
        print("hello")
        print("hello", self)
        serializer = self.get_serializer(pet, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
    def destroy(self, request, pk=None):
        """
        Delete a pet.
        """
        pet = get_object_or_404(Pet, pk=pk, author=request.user)
        pet.delete()
        return Response({"message": "Pet deleted successfully."}, status=204)

class PetSightingCreate(APIView):
    def post(self, request, id):
        """Handles pet sighting creation"""
        
        # Find the pet by its ID
        pet = Pet.objects.filter(id=id).first()
        
        # If the pet does not exist, return an error
        if not pet:
            return Response({"error": "Pet not found"}, status=status.HTTP_404_NOT_FOUND)
        
        # Retrieve the data from the request (make sure it's a valid value)
        status_value = request.data.get('status')  # This should be an integer: 1, 2, or 3
        latitude = request.data.get('latitude')
        longitude = request.data.get('longitude')
        event_occurred_at = request.data.get('event_occurred_at')  # Ensure this is a valid datetime
        notes = request.data.get('notes', '')  # Optional field, default to an empty string
        reporter_id = request.data.get('reporter')  # ID of the reporter
        #image = request.data.get('image')
        image = request.FILES.get('image')  # ✅ Fix: Use `.FILES` for file uploads
        print( request.data)
        # Validate the 'status' field
        try:
        # Convert the status value to an integer
            status_value = int(status_value)
        except (ValueError, TypeError):
            return Response({"error": "Invalid status value"}, status=status.HTTP_400_BAD_REQUEST)

        # Validate if the status_value is valid (present in STATUS_CHOICES)
        if status_value not in dict(PetSightingHistory.STATUS_CHOICES):
            return Response({"error": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST)
        # Find the reporter by the given ID
        reporter = User.objects.filter(id=reporter_id).first()
        print(reporter)
        if not reporter:
            return Response({"error": "Reporter not found"}, status=status.HTTP_404_NOT_FOUND)
        # Ensure latitude and longitude are provided and are valid decimal values
        print(latitude, longitude)
        if not latitude or not longitude:
            return Response({"error": "Latitude and longitude must be provided"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Convert latitude and longitude to Decimal
            latitude = Decimal(latitude)
            longitude = Decimal(longitude)
        except (InvalidOperation, ValueError):
            return Response({"error": "Invalid latitude or longitude format"}, status=status.HTTP_400_BAD_REQUEST)
        
            # Check if event_occurred_at is a valid datetime string and convert it to aware datetime
        if event_occurred_at:
            try:
                # Convert the string to a naive datetime (if it's in ISO format)
                event_occurred_at = datetime.fromisoformat(event_occurred_at)

                # Make it timezone-aware using the current timezone
                event_occurred_at = timezone.make_aware(event_occurred_at, timezone.get_current_timezone())
            except ValueError:
                return Response({"error": "Invalid event_occurred_at format"}, status=status.HTTP_400_BAD_REQUEST)
        
       
        # Create the PetSightingHistory entry
        sighting = PetSightingHistory.objects.create(
            pet=pet,
            status=status_value,
            latitude=latitude,
            longitude=longitude,
            event_occurred_at=event_occurred_at,
            notes=notes,
            # this is a bug, always takes author, should be request user...
            #fix here repoter
            #reporter=pet.author,  # The pet creator is the first sighting reporter
            reporter=request.user,
            image=image
            # reporter=reporter,
        )

        # Return the created sighting data
        return Response({
            "id": sighting.id,
            "pet": sighting.pet.id,
            "status": sighting.get_status_display(),
            "latitude": sighting.latitude,
            "longitude": sighting.longitude,
            "event_occurred_at": sighting.event_occurred_at,
            "notes": sighting.notes,
            "reporter": sighting.reporter.id,
            "image_url": sighting.image.url if sighting.image else None  # Add image URL to the response
        }, status=status.HTTP_201_CREATED)
    



class PetSightingHistoryViewSet(viewsets.ModelViewSet):
    queryset = PetSightingHistory.objects.all()
    serializer_class = PetSightingHistorySerializer
    permission_classes = [IsAuthenticated]  # Ensure only logged-in users can add sightings

    def destroy(self, request, *args, **kwargs):
        sighting_id = kwargs.get('pk')  # Use 'pk' instead of 'sighting_id'
        try:
            sighting = PetSightingHistory.objects.get(id=sighting_id)
            
            # Restrict deletion to the user who reported the sighting
            if sighting.reporter != request.user:
                return Response(
                    {"error": "You are not authorized to delete this sighting"},
                    status=status.HTTP_403_FORBIDDEN
                )

            # If authorized, proceed with deletion
            self.perform_destroy(sighting)
            return Response(
                {"message": "Pet sighting deleted successfully"},
                status=status.HTTP_204_NO_CONTENT
            )

        except PetSightingHistory.DoesNotExist:
            return Response(
                {"error": "Pet sighting not found"},
                status=status.HTTP_404_NOT_FOUND
            )

    def perform_create(self, serializer):
            """ ✅ Ensure that the logged-in user is set as the reporter """
            print("self.request.user", self.request.user)
            serializer.save(reporter=self.request.user)


# Method	Endpoint	Purpose	Status
# GET	/api/pets/	List all pets	✅ Works?
# POST	/api/pets/	Create a new pet	✅ Works?
# GET	/api/pets/1/	Get details of pet ID=1	✅ Works?
# PUT/PATCH	/api/pets/1/	Edit pet ID=1	✅ Works?
# DELETE	/api/pets/1/	Delete pet ID=1	✅ Works?
# GET	/api/user-pets/	Get user’s pets	✅ Works?
# POST	/api/pets/1/pet-sightings/	Create pet sighting	✅ Works?
# GET	/api/pets/1/pet-sightings/	Get all sightings for pet ID=1	✅ Works?
# POST	/api/user-profile/favorite-pets/1/	Add pet ID=1 to favorites	✅ Works?
# DELETE	/api/user-profile/favorite-pets/1/remove/	Remove pet ID=1 from favorites	✅ Works?


# ✔ list – Get all pets (with filters & pagination)
# ✔ retrieve – Get a specific pet
# ✔ create – Add a new pet
# ✔ update – Edit a pet (with PATCH support)
# ✔ destroy – Delete a pet
# ✔ get_user_pets – Get pets created by the logged-in user
# ✔ filtering & searching – By species, age, gender, color, etc.
# ✔ sighting history – Creating and managing pet sightings