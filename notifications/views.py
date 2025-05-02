# from django.shortcuts import render

# # Create your views here.
# # notifications/views.py
# from rest_framework import status
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from .models import PushSubscription
# from .serializers import PushSubscriptionSerializer

# @api_view(['POST'])
# def save_subscription(request):
#     if request.user.is_authenticated:  # Ensure the user is authenticated
#         data = request.data
#         # Create or update the subscription
#         subscription_data = {
#             'user': request.user,
#             'endpoint': data['endpoint'],
#             'p256dh': data['keys']['p256dh'],
#             'auth': data['keys']['auth']
#         }

#         # Use the serializer to validate and save the subscription
#         serializer = PushSubscriptionSerializer(data=subscription_data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'status': 'success'}, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     else:
#         return Response({'error': 'User not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import PushSubscription
from .serializers import PushSubscriptionSerializer
import json
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import PushSubscription
from django.conf import settings
from django.contrib.auth.decorators import login_required
from .models import PushSubscription
import requests
import logging
from pywebpush import webpush, WebPushException

vapid_private_key = settings.WEBPUSH_SETTINGS.get("VAPID_PRIVATE_KEY")
# vapid_public_key = settings.WEBPUSH_SETTINGS.get("VAPID_PUBLIC_KEY")
# vapid_admin_email = settings.WEBPUSH_SETTINGS.get("VAPID_ADMIN_EMAIL")

logger = logging.getLogger(__name__)

VAPID_PRIVATE_KEY = f"{vapid_private_key}"
# VAPID_CLAIMS = {
#     "sub": f"mailto:{vapid_admin_email}"
# }
# VAPID_PRIVATE_KEY = "<your-vapid-private-key>"
# VAPID_CLAIMS = {
#     "sub": "mailto:admin@example.com"
# }
# @csrf_exempt  # Disable CSRF for this view, typically used for API calls
# @login_required  # Ensure the user is authenticated
# def save_subscription(request):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)  # Get the request data as JSON
#             endpoint = data.get('endpoint')
#             p256dh = data.get('p256dh')
#             auth = data.get('auth')

#             if not all([endpoint, p256dh, auth]):
#                 return JsonResponse({"error": "Missing required fields"}, status=400)

#             # Check if the user already has a subscription for this endpoint
#             existing_subscription = PushSubscription.objects.filter(user=request.user, endpoint=endpoint).first()
#             if existing_subscription:
#                 return JsonResponse({"message": "Subscription already exists"}, status=200)

#             # Create a new PushSubscription
#             subscription = PushSubscription(user=request.user, endpoint=endpoint, p256dh=p256dh, auth=auth)
#             subscription.save()

#             return JsonResponse({"message": "Subscription saved successfully"}, status=201)
#         except json.JSONDecodeError:
#             return JsonResponse({"error": "Invalid JSON format"}, status=400)
#     return JsonResponse({"error": "Invalid request method"}, status=405)




# @login_required  # Ensure the user is authenticated
# def unsubscribe(request):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#             endpoint = data.get('endpoint')

#             if not endpoint:
#                 return JsonResponse({"error": "Endpoint is required"}, status=400)

#             # Delete the user's subscription with the given endpoint
#             subscription = PushSubscription.objects.filter(user=request.user, endpoint=endpoint).first()
#             if not subscription:
#                 return JsonResponse({"error": "Subscription not found"}, status=404)

#             subscription.delete()

#             return JsonResponse({"message": "Unsubscribed successfully"}, status=200)

#         except json.JSONDecodeError:
#             return JsonResponse({"error": "Invalid JSON format"}, status=400)
#     return JsonResponse({"error": "Invalid request method"}, status=405)


# @login_required
# def send_notification(request):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#             title = data.get('title')
#             body = data.get('body')
#             url = data.get('url')

#             if not all([title, body]):
#                 return JsonResponse({"error": "Missing required fields: title and body"}, status=400)

#             # Get all subscriptions for the user
#             subscriptions = PushSubscription.objects.filter(user=request.user)
#             if not subscriptions:
#                 return JsonResponse({"error": "No subscriptions found for this user"}, status=404)

#             # For each subscription, send a notification (simplified example)
#             for subscription in subscriptions:
#                 # Replace this with actual push notification logic using the subscription's endpoint, p256dh, and auth
#                 push_data = {
#                     "title": title,
#                     "body": body,
#                     "url": url
#                 }
#                 headers = {
#                     'Content-Type': 'application/json',
#                     # You would need the correct headers and authentication here
#                 }
#                 response = requests.post(subscription.endpoint, json=push_data, headers=headers)
#                 # Check if the response from the push server was successful
#                 if response.status_code != 200:
#                     return JsonResponse({"error": "Failed to send notification"}, status=500)

#             return JsonResponse({"message": "Notification sent successfully"}, status=200)
#         except json.JSONDecodeError:
#             return JsonResponse({"error": "Invalid JSON format"}, status=400)
#     return JsonResponse({"error": "Invalid request method"}, status=405)

from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import PushSubscription
from .serializers import PushSubscriptionSerializer

class PushSubscriptionViewSet(viewsets.ModelViewSet):
    queryset = PushSubscription.objects.all()
    serializer_class = PushSubscriptionSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # Allow public read access, but auth required for write operations

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticatedOrReadOnly])
    def subscribe(self, request):
        """
        Handle the subscription logic (saving or updating the subscription).
        """
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication required."}, status=status.HTTP_401_UNAUTHORIZED)

        subscription_data = request.data
        endpoint = subscription_data.get('endpoint')
        p256dh = subscription_data.get('p256dh')
        auth = subscription_data.get('auth')
        lat = subscription_data.get('lat', 56.946)
        lon = subscription_data.get('lon', 24.1059)
        distance = subscription_data.get('distance', 200.0)

        if not endpoint or not p256dh or not auth:
            return Response({"error": "Missing subscription data."}, status=status.HTTP_400_BAD_REQUEST)

        # Use update_or_create to handle existing devices
        subscription, created = PushSubscription.objects.update_or_create(
            user=request.user,
            endpoint=endpoint,
            defaults={
                'p256dh': p256dh,
                'auth': auth,
                'lat': lat,
                'lon': lon,
                'distance': distance,
            }
        )

        return Response(
            {"message": "Subscription saved!" if created else "Subscription updated."},
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
        )

    
    # Custom action for subscribing (this is already handled by DRF's ModelViewSet `create` method)
    # @action(detail=False, methods=['post'], permission_classes=[IsAuthenticatedOrReadOnly])
    # def subscribe(self, request):
    #     """
    #     Handle the subscription logic (saving the subscription).
    #     """
    #     if not request.user.is_authenticated:
    #         return Response({"detail": "Authentication required."}, status=status.HTTP_401_UNAUTHORIZED)

    #     subscription_data = request.data
    #     subscription = PushSubscription(
    #         user=request.user,
    #         endpoint=subscription_data['endpoint'],
    #         p256dh=subscription_data['p256dh'],
    #         auth=subscription_data['auth']
    #     )
    #     subscription.save()
    #     return Response({"message": "Subscription saved!"}, status=status.HTTP_201_CREATED)


    # Custom action for unsubscribing (removes the subscription from the database)
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticatedOrReadOnly])
    def unsubscribe(self, request):
        """
        Handle the unsubscription logic (removing the subscription).
        """
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication required."}, status=status.HTTP_401_UNAUTHORIZED)

        subscription_data = request.data
        try:
            subscription = PushSubscription.objects.get(endpoint=subscription_data['endpoint'], user=request.user)
            subscription.delete()
            return Response({"message": "Unsubscribed successfully!"}, status=status.HTTP_200_OK)
        except PushSubscription.DoesNotExist:
            return Response({"detail": "Subscription not found."}, status=status.HTTP_404_NOT_FOUND)

    # Send notifications (can be a separate view or action, depending on your use case)
    # @action(detail=False, methods=['post'], permission_classes=[IsAuthenticatedOrReadOnly])
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticatedOrReadOnly])

    # def send_notification(self, request):
    #     @action(detail=False, methods=['post'], permission_classes=[IsAuthenticatedOrReadOnly])
    def send_notification(self, request):
        # """
        # Send notifications to the subscribed users.
        # """
        # Ensure the user is authenticated
            if not request.user.is_authenticated:
                return Response({"detail": "Authentication required."}, status=status.HTTP_401_UNAUTHORIZED)

            # Retrieve notification data
            data = request.data
            title = data.get('title')
            body = data.get('body')
            url = data.get('url')

            # Ensure title and body are provided
            if not all([title, body]):
                return Response({"error": "Missing required fields: title and body"}, status=status.HTTP_400_BAD_REQUEST)

            # Get all subscriptions for the user
            subscriptions = PushSubscription.objects.filter(user=request.user)
            if not subscriptions:
                return Response({"error": "No subscriptions found for this user"}, status=status.HTTP_404_NOT_FOUND)

            # Create notification payload
            payload = json.dumps({
                "title": title,
                "body": body,
                "url": url
            })

            failures = []

            # Loop through each subscription and send the push notification
            for subscription in subscriptions:
                try:
                    logger.info(f"Sending push notification to {subscription.endpoint}")
                    
                    # Sending the push notification via webpush
                    webpush(
                        subscription_info={
                            "endpoint": subscription.endpoint,
                            "keys": {
                                "p256dh": subscription.p256dh,
                                "auth": subscription.auth
                            }
                        },
                        data=payload,
                        vapid_private_key=settings.WEBPUSH_SETTINGS['VAPID_PRIVATE_KEY'],
                        # vapid_claims=settings.WEBPUSH_SETTINGS['VAPID_ADMIN_EMAIL']
                        vapid_claims={
        "sub": f"mailto:{settings.WEBPUSH_SETTINGS['VAPID_ADMIN_EMAIL']}"
    }
                    )
                except WebPushException as ex:
                    logger.error(f"Push failed for endpoint {subscription.endpoint}: {str(ex)}")
                    failures.append(subscription.endpoint)

            if failures:
                return Response({
                    "error": "Some notifications failed.",
                    "failed_endpoints": failures
                }, status=status.HTTP_207_MULTI_STATUS)

            return Response({"message": "Notification sent successfully!"}, status=status.HTTP_200_OK)