# from django.urls import path
# from . import views

# urlpatterns = [
#     path('subscribe/', views.save_subscription, name='save_subscription'),
#     path('unsubscribe/', views.unsubscribe, name='unsubscribe'),
#     path('send/', views.send_notification, name='send_notification'),
# ]
# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from .views import PushSubscriptionViewSet

# # Create a router and register the viewset with it
# router = DefaultRouter()
# router.register(r'', PushSubscriptionViewSet, basename='push-subscription')

# urlpatterns = [
#     path('', include(router.urls)),  # This will generate the routes for subscribe, unsubscribe, and send_notification
# ]

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PushSubscriptionViewSet

# Create a router and register the PushSubscriptionViewSet
router = DefaultRouter()
router.register(r'', PushSubscriptionViewSet, basename='push-subscription')

urlpatterns = [
    path('', include(router.urls)),  # This will automatically generate the routes for subscribe, unsubscribe, and send_notification
]
