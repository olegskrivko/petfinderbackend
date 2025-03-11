from rest_framework import serializers
from .models import Shelter, SocialMedia

class SocialMediaSerializer(serializers.ModelSerializer):
    platform = serializers.CharField(source='get_platform_display', read_only=True)
    class Meta:
        model = SocialMedia
        fields = ['platform', 'profile_url']

class ShelterSerializer(serializers.ModelSerializer):
        # Serialize the social media names
    
    social_media = SocialMediaSerializer(many=True, read_only=True)
    class Meta:
        model = Shelter
        fields = [
            'id', 
            'name', 
            'description', 
            'website', 
            'country', 
            'region', 
            'city', 
            'street', 
            'postal_code', 
            'latitude', 
            'longitude', 
            'full_address', 
            'phone_number', 
            'phone_code',
            'email',
            'social_media',  # Add social media to the serialized fields
        ]
