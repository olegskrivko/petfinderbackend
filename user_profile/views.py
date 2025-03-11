from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from pets.models import Pet
from pets.serializers import PetSerializer
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from pets.models import Pet
from pets.models import UserFavorites
from django.shortcuts import get_object_or_404

# View to get pets owned by the authenticated user
class UserPetsView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated

    def get(self, request):
        user = request.user  # Get the logged-in user
        pets = Pet.objects.filter(author=user)  # Fetch pets created by this user
        
        # Serialize the pets data
        serializer = PetSerializer(pets, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)

# View to delete a specific pet owned by the authenticated user
class DeletePetView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated

    def delete(self, request, pet_id):
        try:
            pet = Pet.objects.get(id=pet_id, author=request.user)  # Fetch pet by id and ensure the user is the owner
        except Pet.DoesNotExist:
            raise NotFound(detail="Pet not found or you do not have permission to delete it.")

        pet.delete()  # Delete the pet
        return Response({"detail": "Pet deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    

class GetFavoritedPets(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        # Get all pets that the user has favorited
        favorite_pets = UserFavorites.objects.filter(user=user).select_related('pet')

        # Serialize the pet data
        pets = [favorite.pet for favorite in favorite_pets]
        serialized_pets = PetSerializer(pets, many=True)

        return Response(serialized_pets.data, status=status.HTTP_200_OK)

# class FavoritePetView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request, pet_id):
#         user = request.user
#         try:
#             pet = Pet.objects.get(id=pet_id)
#         except Pet.DoesNotExist:
#             return Response({"detail": "Pet not found."}, status=status.HTTP_404_NOT_FOUND)

#         # Check if the pet is already in favorites
#         if UserFavorites.objects.filter(user=user, pet=pet).exists():
#             return Response({"detail": "Pet is already in favorites."}, status=status.HTTP_400_BAD_REQUEST)

#         # Add to favorites
#         UserFavorites.objects.create(user=user, pet=pet)
#         return Response({"detail": "Pet added to favorites."}, status=status.HTTP_201_CREATED)

#     def delete(self, request, pet_id):
#         user = request.user
#         try:
#             pet = Pet.objects.get(id=pet_id)
#         except Pet.DoesNotExist:
#             return Response({"detail": "Pet not found."}, status=status.HTTP_404_NOT_FOUND)

#         # Check if the pet is in favorites
#         favorite = UserFavorites.objects.filter(user=user, pet=pet).first()
#         if not favorite:
#             return Response({"detail": "Pet is not in favorites."}, status=status.HTTP_400_BAD_REQUEST)

#         # Remove from favorites
#         favorite.delete()
#         return Response({"detail": "Pet removed from favorites."}, status=status.HTTP_204_NO_CONTENT)


# View to add/remove a pet from favorites
# class FavoritePetView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request, pet_id):
#         user = request.user
#         pet = get_object_or_404(Pet, id=pet_id)

#         # Check if already favorited
#         if UserFavorites.objects.filter(user=user, pet=pet).exists():
#             return Response({"detail": "Pet is already in favorites."}, status=status.HTTP_400_BAD_REQUEST)

#         # Add to favorites
#         UserFavorites.objects.create(user=user, pet=pet)
#         return Response({"detail": "Pet added to favorites."}, status=status.HTTP_201_CREATED)

# class FavoritePetView(APIView):
#     def post(self, request, pet_id):
#         """Add a pet to the user's favorites."""
#         user_profile = request.user.profile  # Assuming profile is linked to user
#         pet = Pet.objects.get(id=pet_id)
        
#         if pet in user_profile.favorited_pets.all():
#             return Response({"detail": "Pet is already in favorites."}, status=status.HTTP_400_BAD_REQUEST)

#         user_profile.favorited_pets.add(pet)
#         return Response({"detail": "Pet added to favorites."}, status=status.HTTP_201_CREATED)

#     def delete(self, request, pet_id):
#         """Remove a pet from favorites."""
#         user_profile = request.user.profile
#         pet = Pet.objects.filter(id=pet_id).first()

#         if not pet or pet not in user_profile.favorited_pets.all():
#             return Response({"detail": "Pet is not in favorites."}, status=status.HTTP_404_NOT_FOUND)

#         user_profile.favorited_pets.remove(pet)
#         return Response({"detail": "Pet removed from favorites."}, status=status.HTTP_204_NO_CONTENT)
class FavoritePetView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pet_id):
        """Check if a pet is in the user's favorites."""
        user = request.user
        pet = get_object_or_404(Pet, id=pet_id)

        # Check if the pet is favorited
        is_favorite = UserFavorites.objects.filter(user=user, pet=pet).exists()
        return Response({"is_favorite": is_favorite}, status=status.HTTP_200_OK)

    def post(self, request, pet_id):
        """Add a pet to the user's favorites."""
        user = request.user
        pet = get_object_or_404(Pet, id=pet_id)

        # Check if already favorited
        if UserFavorites.objects.filter(user=user, pet=pet).exists():
            return Response({"detail": "Pet is already in favorites."}, status=status.HTTP_400_BAD_REQUEST)

        # Add to favorites
        UserFavorites.objects.create(user=user, pet=pet)
        return Response({"detail": "Pet added to favorites."}, status=status.HTTP_201_CREATED)

    def delete(self, request, pet_id):
        """Remove a pet from the user's favorites."""
        user = request.user
        pet = get_object_or_404(Pet, id=pet_id)

        # Check if pet is in favorites
        favorite = UserFavorites.objects.filter(user=user, pet=pet)
        if not favorite.exists():
            return Response({"detail": "Pet is not in favorites."}, status=status.HTTP_404_NOT_FOUND)

        # Remove from favorites
        favorite.delete()
        return Response({"detail": "Pet removed from favorites."}, status=status.HTTP_204_NO_CONTENT)
# View to remove a favorited pet
class UnfavoritePetView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pet_id):
        user = request.user
        favorite_pet = get_object_or_404(UserFavorites, pet_id=pet_id, user=user)
        favorite_pet.delete()
        return Response({"message": "Pet removed from favorites"}, status=status.HTTP_204_NO_CONTENT)