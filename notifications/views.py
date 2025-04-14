from django.shortcuts import render

# Create your views here.
# notifications/views.py
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import PushSubscription
from .serializers import PushSubscriptionSerializer

@api_view(['POST'])
def save_subscription(request):
    if request.user.is_authenticated:  # Ensure the user is authenticated
        data = request.data
        # Create or update the subscription
        subscription_data = {
            'user': request.user,
            'endpoint': data['endpoint'],
            'p256dh': data['keys']['p256dh'],
            'auth': data['keys']['auth']
        }

        # Use the serializer to validate and save the subscription
        serializer = PushSubscriptionSerializer(data=subscription_data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'success'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error': 'User not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
