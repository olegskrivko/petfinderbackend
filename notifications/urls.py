# notifications/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('subscribe/', views.save_subscription, name='save_subscription'),
]
