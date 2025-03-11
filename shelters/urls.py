# from django.urls import path
# from . import views

# urlpatterns = [
#     path('', views.shelter_list, name='shelter_list'),
#     path('<int:pk>/', views.shelter_detail, name='shelter_detail'),
# ]


# pets/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ShelterViewSet

router = DefaultRouter()
router.register(r'', ShelterViewSet)

urlpatterns = [
    path('', include(router.urls)),  # Register PetViewSet in the API
]
