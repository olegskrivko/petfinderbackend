# notifications/serializers.py
from rest_framework import serializers
from .models import PushSubscription

class PushSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PushSubscription
        fields = ['user', 'endpoint', 'p256dh', 'auth']

    def create(self, validated_data):
        return PushSubscription.objects.create(**validated_data)
