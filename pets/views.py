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
# from django.contrib.auth.models import User
from decimal import Decimal, InvalidOperation
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from rest_framework.permissions import BasePermission
from decimal import Decimal
from django.utils.timezone import now
from rest_framework.parsers import MultiPartParser, FormParser
import cloudinary.uploader
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from rest_framework.exceptions import ValidationError
User = get_user_model()

class PetFilter(filters.FilterSet):
    status = filters.NumberFilter(field_name='status', lookup_expr='exact')
    species = filters.NumberFilter(field_name='species', lookup_expr='exact')
    age = filters.NumberFilter(field_name='age', lookup_expr='exact')  # Filter for age (exact match)
    gender = filters.NumberFilter(field_name='gender', lookup_expr='exact')  # Filter for gender
    size = filters.NumberFilter(field_name='size', lookup_expr='exact')  # Filter for size
    pattern = filters.NumberFilter(field_name='pattern', lookup_expr='exact')  # Filter for size
    date = filters.IsoDateTimeFilter(field_name='event_occurred_at', lookup_expr='gte', label="Filter by Event Date")

    # Allow searching on name and notes
    search_fields = ['name', 'notes']  # Fields you want to allow search on

    color = filters.NumberFilter(method='filter_by_color')

    def filter_by_color(self, queryset, name, value):
        # Filter pets by either primary_color or secondary_color matching the selected color
        return queryset.filter(
            Q(primary_color=value) | Q(secondary_color=value)
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
    print("i am in petviewset")
    queryset = Pet.objects.all().order_by('id')  # Adjust query if no longer using PetSightingHistory
    serializer_class = PetSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_class = PetFilter
    pagination_class = PetPagination
    parser_classes = (MultiPartParser, FormParser)

    def perform_create(self, serializer):

        uploaded_images = {}
        uploaded_images_list = []  # Store uploaded images in order

        # Handle image uploads (at least one required)
        for i in range(1, 5):  # Loop from pet_image_1 to pet_image_4
            image_field = f"pet_image_{i}_media"  # Field name from request
            image = self.request.FILES.get(image_field)

            if image:
                uploaded_image = cloudinary.uploader.upload(image)
                uploaded_images_list.append(uploaded_image.get("secure_url"))

        # Ensure at least one image is uploaded
        if not uploaded_images_list:
            raise ValidationError({"error": "At least one image must be uploaded."})

        # Assign images sequentially to pet_image_1, pet_image_2, etc.
        for index, image_url in enumerate(uploaded_images_list):
            uploaded_images[f"pet_image_{index+1}"] = image_url  # Assign in order

        # Fill remaining image fields with None
        for i in range(len(uploaded_images_list) + 1, 5):  # Ensure all 4 fields exist
            uploaded_images[f"pet_image_{i}"] = None
        # image_1 = self.request.FILES.get('pet_image_1_media')
        # image_2 = self.request.FILES.get('pet_image_2_media')
        # image_3 = self.request.FILES.get('pet_image_3_media')
        # image_4 = self.request.FILES.get('pet_image_4_media')
        # uploaded_image_1_url = None
        # uploaded_image_2_url = None
        # uploaded_image_3_url = None
        # uploaded_image_4_url = None
        # if image_1:
        #     uploaded_image_1 = cloudinary.uploader.upload(image_1)
        #     uploaded_image_1_url = uploaded_image_1.get("secure_url")
        # if image_2:
        #     uploaded_image_2 = cloudinary.uploader.upload(image_2)
        #     uploaded_image_2_url = uploaded_image_2.get("secure_url")
        # if image_3:
        #     uploaded_image_3 = cloudinary.uploader.upload(image_3)
        #     uploaded_image_3_url = uploaded_image_3.get("secure_url")
        # if image_4:
        #     uploaded_image_4 = cloudinary.uploader.upload(image_4)
        #     uploaded_image_4_url = uploaded_image_4.get("secure_url")

            # Get date and time from request
        date = self.request.data.get("date")  # e.g., "2025-04-01"
        time = self.request.data.get("time")  # e.g., "14:30"
        print("date", self.request.data.get("date"))

        if date and time:
            try:
                # Combine date and time into a single string
                combined_datetime_str = f"{date} {time}"
                # Parse the combined string into a datetime object
                event_occurred_at = datetime.strptime(combined_datetime_str, "%Y-%m-%d %H:%M")
                # Make it timezone-aware
                event_occurred_at = make_aware(event_occurred_at)
            except ValueError:
                event_occurred_at = timezone.now()  # Default to now if the date/time is invalid
        else:
            event_occurred_at = timezone.now()  # Default to now if missing

        pet = serializer.save(
            author=self.request.user,
            # pet_image_1=uploaded_image_1_url,
            # pet_image_2=uploaded_image_2_url,
            # pet_image_3=uploaded_image_3_url,
            # pet_image_4=uploaded_image_4_url,
            event_occurred_at=event_occurred_at,
             **uploaded_images  # Dynamically assign images
        )

    def retrieve(self, request, pk=None):
        pet = get_object_or_404(Pet, pk=pk)
        serializer = self.get_serializer(pet)
        return Response(serializer.data)
    
    def update(self, request, pk=None):
        pet = get_object_or_404(Pet, pk=pk, author=request.user)
        serializer = self.get_serializer(pet, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
    def destroy(self, request, pk=None):
        pet = get_object_or_404(Pet, pk=pk, author=request.user)
        pet.delete()
        return Response({"message": "Pet deleted successfully."}, status=204)
# class PetSightingCreate(APIView):
#     """Handles creating a pet sighting entry"""

#     def post(self, request, id):
#         # ✅ Find the pet by ID or return 404
#         pet = get_object_or_404(Pet, id=id)

#         # ✅ Extract data from request
#         status_value = request.data.get('status')
#         latitude = request.data.get('latitude')
#         longitude = request.data.get('longitude')
#         notes = request.data.get('notes', '')
#         reporter = request.user  # ✅ Ensure it's linked to the authenticated user

#         # ✅ Get and process date/time
#         date = request.data.get("date")  # e.g., "2025-04-01"
#         time = request.data.get("time")  # e.g., "14:30"

#         if date and time:
#             try:
#                 combined_datetime_str = f"{date} {time}"
#                 event_occurred_at = datetime.strptime(combined_datetime_str, "%Y-%m-%d %H:%M")
#                 event_occurred_at = make_aware(event_occurred_at)  # Convert to timezone-aware
#             except ValueError:
#                 return Response({"error": "Invalid date or time format"}, status=status.HTTP_400_BAD_REQUEST)
#         else:
#             event_occurred_at = timezone.now()  # Default to now if missing

#         # ✅ Validate `status`
#         try:
#             status_value = int(status_value)
#             if status_value not in dict(PetSightingHistory.STATUS_CHOICES):
#                 return Response({"error": "Invalid status value"}, status=status.HTTP_400_BAD_REQUEST)
#         except (ValueError, TypeError):
#             return Response({"error": "Invalid status format"}, status=status.HTTP_400_BAD_REQUEST)

#         # ✅ Validate & convert latitude/longitude
#         if latitude and longitude:
#             try:
#                 latitude = Decimal(latitude)
#                 longitude = Decimal(longitude)
#             except (InvalidOperation, ValueError):
#                 return Response({"error": "Invalid latitude or longitude format"}, status=status.HTTP_400_BAD_REQUEST)
#         else:
#             return Response({"error": "Latitude and longitude are required"}, status=status.HTTP_400_BAD_REQUEST)

#         # ✅ Handle image upload (if provided)
#         image_url = None
#         image = request.FILES.get('image')
#         print("imagexxx", image)
#         if image:
#             uploaded_image = cloudinary.uploader.upload(image)
#             image_url = uploaded_image.get("secure_url")

#         # ✅ Save the pet sighting in the database
#         sighting = PetSightingHistory.objects.create(
#             pet=pet,
#             status=status_value,
#             latitude=latitude,
#             longitude=longitude,
#             event_occurred_at=event_occurred_at,
#             notes=notes,
#             reporter=reporter,
#             pet_image=image_url  # ✅ Store uploaded image URL
#         )

#         # ✅ Return success response
#         return Response({
#             "id": sighting.id,
#             "pet": sighting.pet.id,
#             "status": sighting.get_status_display(),
#             "latitude": sighting.latitude,
#             "longitude": sighting.longitude,
#             "event_occurred_at": sighting.event_occurred_at,
#             "notes": sighting.notes,
#             "image": sighting.pet_image,
#             "reporter": sighting.reporter.id,
#         }, status=status.HTTP_201_CREATED)
# class PetSightingCreate(APIView):
#     parser_classes = (MultiPartParser, FormParser)  # ✅ Allow image uploads
#     def post(self, request, id):
#         """Handles pet sighting creation"""
        
#         # Find pet by ID or return 404
#         pet = get_object_or_404(Pet, id=id)

#         # Extract data from request
#         status_value = request.data.get('status')
#         latitude = request.data.get('latitude')
#         longitude = request.data.get('longitude')
#         date = request.data.get('date')  # e.g., "2025-04-01"
#         time = request.data.get('time')  # e.g., "14:30"
#         notes = request.data.get('notes', '')
#         image = request.FILES.get('image')  # ✅ Fix: Handle image uploads

#         # Validate `status`
#         try:
#             status_value = int(status_value)
#             if status_value not in dict(PetSightingHistory.STATUS_CHOICES):
#                 return Response({"error": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST)
#         except (ValueError, TypeError):
#             return Response({"error": "Invalid status value"}, status=status.HTTP_400_BAD_REQUEST)

#         # ✅ Validate `latitude` and `longitude`
#         if not latitude or not longitude:
#             return Response({"error": "Latitude and longitude are required"}, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             latitude = Decimal(latitude)
#             longitude = Decimal(longitude)
#         except (InvalidOperation, ValueError):
#             return Response({"error": "Invalid latitude or longitude format"}, status=status.HTTP_400_BAD_REQUEST)

#         # ✅ Combine `date` and `time` into `event_occurred_at`
#         if date and time:
#             try:
#                 combined_datetime_str = f"{date} {time}"
#                 event_occurred_at = datetime.strptime(combined_datetime_str, "%Y-%m-%d %H:%M")
#                 event_occurred_at = make_aware(event_occurred_at)
#             except ValueError:
#                 return Response({"error": "Invalid date or time format"}, status=status.HTTP_400_BAD_REQUEST)
#         else:
#             event_occurred_at = timezone.now()  # Default to current time if missing

#        # ✅ Upload image to Cloudinary (if provided)
#         uploaded_image_url = None
#         if image:
#             try:
#                 uploaded_image = cloudinary.uploader.upload(image)
#                 uploaded_image_url = uploaded_image.get("secure_url")
#             except Exception as e:
#                 return Response({"error": f"Image upload failed: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#         # ✅ Create the PetSightingHistory entry
#         sighting = PetSightingHistory.objects.create(
#             pet=pet,
#             status=status_value,
#             latitude=latitude,
#             longitude=longitude,
#             event_occurred_at=event_occurred_at,
#             notes=notes,
#             reporter=request.user,  # ✅ Always use `request.user`
#             image=uploaded_image_url  # ✅ Save Cloudinary image URL
#         )

#         # ✅ Return success response
#         return Response({
#             "id": sighting.id,
#             "pet": sighting.pet.id,
#             "status": sighting.get_status_display(),
#             "latitude": sighting.latitude,
#             "longitude": sighting.longitude,
#             "event_occurred_at": sighting.event_occurred_at,
#             "notes": sighting.notes,
#             "reporter": sighting.reporter.id,
#             "image_url": uploaded_image_url  # ✅ Include image URL in response
#         }, status=status.HTTP_201_CREATED)
# class PetSightingView(APIView):
#     """Handles creating pet sighting entry (POST) and listing pet sighting entries (GET)"""

#     def get(self, request, id):
#         # List pet sightings for a specific pet
#         pet = get_object_or_404(Pet, id=id)
#         sightings = PetSightingHistory.objects.filter(pet=pet)
#         serializer = PetSightingHistorySerializer(sightings, many=True)
#         return Response(serializer.data)

#     def post(self, request, id):
#         # Create a new pet sighting entry
#         pet = get_object_or_404(Pet, id=id)

#         status_value = request.data.get('status')
#         latitude = request.data.get('latitude')
#         longitude = request.data.get('longitude')
#         notes = request.data.get('notes', '')
#         reporter = request.user

#         # Get and process date/time
#         date = request.data.get("date")  # e.g., "2025-04-01"
#         time = request.data.get("time")  # e.g., "14:30"

#         if date and time:
#             try:
#                 combined_datetime_str = f"{date} {time}"
#                 event_occurred_at = datetime.strptime(combined_datetime_str, "%Y-%m-%d %H:%M")
#                 event_occurred_at = make_aware(event_occurred_at)  # Convert to timezone-aware
#             except ValueError:
#                 return Response({"error": "Invalid date or time format"}, status=status.HTTP_400_BAD_REQUEST)
#         else:
#             event_occurred_at = timezone.now()  # Default to now if missing

#         # Validate `status`
#         try:
#             status_value = int(status_value)
#             if status_value not in dict(PetSightingHistory.STATUS_CHOICES):
#                 return Response({"error": "Invalid status value"}, status=status.HTTP_400_BAD_REQUEST)
#         except (ValueError, TypeError):
#             return Response({"error": "Invalid status format"}, status=status.HTTP_400_BAD_REQUEST)

#         # Validate latitude/longitude
#         if latitude and longitude:
#             try:
#                 latitude = Decimal(latitude)
#                 longitude = Decimal(longitude)
#             except (InvalidOperation, ValueError):
#                 return Response({"error": "Invalid latitude or longitude format"}, status=status.HTTP_400_BAD_REQUEST)
#         else:
#             return Response({"error": "Latitude and longitude are required"}, status=status.HTTP_400_BAD_REQUEST)

#         # Handle image upload (if provided)
#         image_url = None
#         image = request.FILES.get('image')
#         if image:
#             uploaded_image = cloudinary.uploader.upload(image)
#             image_url = uploaded_image.get("secure_url")

#         # Save the pet sighting in the database
#         sighting = PetSightingHistory.objects.create(
#             pet=pet,
#             status=status_value,
#             latitude=latitude,
#             longitude=longitude,
#             event_occurred_at=event_occurred_at,
#             notes=notes,
#             reporter=reporter,
#             pet_image=image_url
#         )

#         # Return success response
#         return Response({
#             "id": sighting.id,
#             "pet": sighting.pet.id,
#             "status": sighting.get_status_display(),
#             "latitude": sighting.latitude,
#             "longitude": sighting.longitude,
#             "event_occurred_at": sighting.event_occurred_at,
#             "notes": sighting.notes,
#             "image": sighting.pet_image,
#             "reporter": sighting.reporter.id,
#         }, status=status.HTTP_201_CREATED)  


# class PetSightingHistoryViewSet(viewsets.ModelViewSet):
#     queryset = PetSightingHistory.objects.all()
#     serializer_class = PetSightingHistorySerializer
#     permission_classes = [IsAuthenticated]  # Ensure only logged-in users can add sightings

#     def destroy(self, request, *args, **kwargs):
#         sighting_id = kwargs.get('pk')  # Use 'pk' instead of 'sighting_id'
#         try:
#             sighting = PetSightingHistory.objects.get(id=sighting_id)
            
#             # Restrict deletion to the user who reported the sighting
#             if sighting.reporter != request.user:
#                 return Response(
#                     {"error": "You are not authorized to delete this sighting"},
#                     status=status.HTTP_403_FORBIDDEN
#                 )

#             # If authorized, proceed with deletion
#             self.perform_destroy(sighting)
#             return Response(
#                 {"message": "Pet sighting deleted successfully"},
#                 status=status.HTTP_204_NO_CONTENT
#             )

#         except PetSightingHistory.DoesNotExist:
#             return Response(
#                 {"error": "Pet sighting not found"},
#                 status=status.HTTP_404_NOT_FOUND
#             )

#     def perform_create(self, serializer):
#             """ ✅ Ensure that the logged-in user is set as the reporter """
#             print("self.request.user", self.request.user)
#             serializer.save(reporter=self.request.user)
class PetSightingView(APIView):
    """Handles creating pet sighting entry (POST), listing pet sightings (GET), and deleting a sighting (DELETE)"""

    def get(self, request, id):
        # List pet sightings for a specific pet
        pet = get_object_or_404(Pet, id=id)
        sightings = PetSightingHistory.objects.filter(pet=pet)
        serializer = PetSightingHistorySerializer(sightings, many=True)
        return Response(serializer.data)

    def post(self, request, id):
        # Create a new pet sighting entry
        pet = get_object_or_404(Pet, id=id)

        status_value = request.data.get('status')
        latitude = request.data.get('latitude')
        longitude = request.data.get('longitude')
        notes = request.data.get('notes', '')
        reporter = request.user

        # Get and process date/time
        date = request.data.get("date")  # e.g., "2025-04-01"
        time = request.data.get("time")  # e.g., "14:30"

        if date and time:
            try:
                combined_datetime_str = f"{date} {time}"
                event_occurred_at = datetime.strptime(combined_datetime_str, "%Y-%m-%d %H:%M")
                event_occurred_at = timezone.make_aware(event_occurred_at)  # Convert to timezone-aware
            except ValueError:
                return Response({"error": "Invalid date or time format"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            event_occurred_at = timezone.now()  # Default to now if missing

        # Validate `status`
        try:
            status_value = int(status_value)
            if status_value not in dict(PetSightingHistory.STATUS_CHOICES):
                return Response({"error": "Invalid status value"}, status=status.HTTP_400_BAD_REQUEST)
        except (ValueError, TypeError):
            return Response({"error": "Invalid status format"}, status=status.HTTP_400_BAD_REQUEST)

        # Validate latitude/longitude
        if latitude and longitude:
            try:
                latitude = Decimal(latitude)
                longitude = Decimal(longitude)
            except (InvalidOperation, ValueError):
                return Response({"error": "Invalid latitude or longitude format"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Latitude and longitude are required"}, status=status.HTTP_400_BAD_REQUEST)

        # Handle image upload (if provided)
        image_url = None
        image = request.FILES.get('image')
        if image:
            uploaded_image = cloudinary.uploader.upload(image)
            image_url = uploaded_image.get("secure_url")

        # Save the pet sighting in the database
        sighting = PetSightingHistory.objects.create(
            pet=pet,
            status=status_value,
            latitude=latitude,
            longitude=longitude,
            event_occurred_at=event_occurred_at,
            notes=notes,
            reporter=reporter,
            pet_image=image_url
        )

        # Return success response
        return Response({
            "id": sighting.id,
            "pet": sighting.pet.id,
            "status": sighting.get_status_display(),
            "latitude": sighting.latitude,
            "longitude": sighting.longitude,
            "event_occurred_at": sighting.event_occurred_at,
            "notes": sighting.notes,
            "image": sighting.pet_image,
            "reporter": sighting.reporter.id,
        }, status=status.HTTP_201_CREATED)

    def delete(self, request, id, sighting_id):
        """
        Delete a pet sighting entry.
        Only the user who reported the sighting (sighting.reporter) can delete it.
        """
        # Get the pet instance by its ID
        pet = get_object_or_404(Pet, id=id)
        
        # Get the pet sighting instance by its ID and ensure it belongs to the pet
        sighting = get_object_or_404(PetSightingHistory, id=sighting_id, pet=pet)

        # Ensure that only the user who reported the sighting can delete it
        if sighting.reporter != request.user:
            raise PermissionDenied("You are not authorized to delete this sighting.")

        # Perform the deletion
        sighting.delete()

        return Response({"message": "Pet sighting deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    # def delete(self, request, id, sighting_id):
    #     # Delete a pet sighting entry
    #     pet = get_object_or_404(Pet, id=id)
    #     sighting = get_object_or_404(PetSightingHistory, id=sighting_id, pet=pet)

    #     # Ensure that only the user who reported the sighting can delete it
    #     if sighting.reporter != request.user:
    #         raise PermissionDenied("You are not authorized to delete this sighting.")

    #     # Perform the deletion
    #     sighting.delete()
    #     return Response({"message": "Pet sighting deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    
class RecentPetsView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            # Assuming you want the most recent pets based on some ordering criteria
            recent_pets = Pet.objects.all().order_by('-created_at')[:4]  # Adjust based on your criteria
            serializer = PetSerializer(recent_pets, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
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