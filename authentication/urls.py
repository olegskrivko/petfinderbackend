from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('user/', views.get_user_details, name='user-details'),  # ✅ New endpoint
    path("user/delete/", views.delete_user, name="delete-user"),
]
