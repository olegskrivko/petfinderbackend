# services/serializers.py
from rest_framework import serializers
from .models import Service, Location, WorkingHour, Review, SocialMedia

class WorkingHourSerializer(serializers.ModelSerializer):
    day_display = serializers.CharField(source='get_day_display')

    class Meta:
        model = WorkingHour
        fields = '__all__' 

class LocationSerializer(serializers.ModelSerializer):
    working_hours = WorkingHourSerializer(many=True, read_only=True)
    latitude = serializers.DecimalField(max_digits=9, decimal_places=6, required=True)
    longitude = serializers.DecimalField(max_digits=9, decimal_places=6, required=True)

    class Meta:
        model = Location
        fields = '__all__' 
        # fields = ['id', 'city', 'address', 'phone_number', 'email', 'working_hours']

class SocialMediaSerializer(serializers.ModelSerializer):
    platform = serializers.CharField(source='get_platform_display', read_only=True)
    class Meta:
        model = SocialMedia
        fields = ['platform', 'profile_url']

class ServiceSerializer(serializers.ModelSerializer):
    locations = LocationSerializer(many=True)
    user = serializers.ReadOnlyField(source='user.username')  # Optional: Display username
    category_display = serializers.CharField(source='get_category_display', read_only=True)  # 👈 Add this
    provider_type_display = serializers.CharField(source='get_provider_type_display', read_only=True)
    price_type_display = serializers.CharField(source='get_price_type_display', read_only=True)
    average_rating = serializers.FloatField(source='get_average_rating', read_only=True)
    social_media = SocialMediaSerializer(many=True, read_only=True)
    # tags = serializers.CharField(source='get_tags_display', read_only=True)
    # reviews = ReviewSerializer(many=True, read_only=True)  # Uncomment if you want reviews in the service detail

    class Meta:
        model = Service
        fields = '__all__' 
        
        # fields = ['id', 'title', 'description', 'price', 'category', 'created_at', 'user', 'locations']

    def create(self, validated_data):
        locations_data = validated_data.pop('locations')
        service = Service.objects.create(**validated_data)
        for location_data in locations_data:
            Location.objects.create(service=service, **location_data)
        return service

    def update(self, instance, validated_data):
        locations_data = validated_data.pop('locations', None)

        # Update basic service fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        if locations_data:
            # Delete old locations and recreate new ones (simplified)
            instance.locations.all().delete()
            for location_data in locations_data:
                Location.objects.create(service=instance, **location_data)

        return instance
    


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'user', 'rating', 'comment', 'created_at']

