# core/serializers.py

from rest_framework import serializers
from .models import SocialMedia  # Add SocialMedia model import if required

# class CountrySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Country
#         fields = [
#             'id',
#             'name',
#             'country_code',
#             'capital',
#             'currency',
#             'language',
#             'phone_code',
#         ]

class SocialMediaSerializer(serializers.ModelSerializer):
    platform_name = serializers.CharField(source='get_platform_display', read_only=True)  # Automatically converts integer to name

    class Meta:
        model = SocialMedia
        fields = ['id', 'platform', 'platform_name', 'profile_url', 'is_official', 'is_verified']