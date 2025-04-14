# # services/serializers.py
# from rest_framework import serializers
# from .models import Service

# class ServiceSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Service
#         fields = ['id', 'title', 'description', 'price', 'category', 'created_at']
# services/serializers.py
from rest_framework import serializers
from .models import Service, Location

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['id', 'city', 'address', 'phone_number', 'email']

class ServiceSerializer(serializers.ModelSerializer):
    locations = LocationSerializer(many=True)  # Include locations in service serializer

    class Meta:
        model = Service
        fields = ['id', 'title', 'description', 'price', 'category', 'created_at', 'locations']
