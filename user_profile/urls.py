from django.urls import path
from . import views

urlpatterns = [
    # Pets owned by the authenticated user
    path('user-pets/', views.UserPetsView.as_view(), name='user_pets'),
    path('user-pets/<int:pet_id>/delete/', views.DeletePetView.as_view(), name='delete_pet'),

    # Favorite pets - Adding and removing from the pet details page
    path('favorite-pets/<int:pet_id>/', views.FavoritePetView.as_view(), name='favorite_pet'),

    # Getting and removing favorites from user profile
    path('favorite-pets/', views.GetFavoritedPets.as_view(), name='get_favorited_pets'),  # GET all favorited pets
    path('favorite-pets/<int:pet_id>/remove/', views.UnfavoritePetView.as_view(), name='unfavorite_pet'),  # DELETE

    # Route to get pets that are favorited by the user
    # path('favorited-pets/', views.GetFavoritedPets.as_view(), name='get_favorited_pets'),
    # path('favorited-pets/<int:pet_id>/delete/', views.UnfavoritePetView.as_view(), name='unfavorite_pet'),

    
    
    
]