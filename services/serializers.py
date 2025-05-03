# services/serializers.py
from rest_framework import serializers
from .models import Service, Location, WorkingHour, Review, SocialMedia

class WorkingHourSerializer(serializers.ModelSerializer):
    day_display = serializers.CharField(source='get_day_display')

    class Meta:
        model = WorkingHour
        fields = '__all__' 
# correct was workign
# class LocationSerializer(serializers.ModelSerializer):
#     working_hours = WorkingHourSerializer(many=True, read_only=True)
#     latitude = serializers.DecimalField(max_digits=9, decimal_places=6, required=True)
#     longitude = serializers.DecimalField(max_digits=9, decimal_places=6, required=True)

#     class Meta:
#         model = Location
#         fields = '__all__' 

class LocationSerializer(serializers.ModelSerializer):
    working_hours = WorkingHourSerializer(many=True)

    class Meta:
        model = Location
        fields = '__all__'

    def create(self, validated_data):
        # Extract the nested working_hours data
        working_hours_data = validated_data.pop('working_hours', [])
        # Create the Location object
        location = Location.objects.create(**validated_data)
        # Create the working hours for the location
        for wh_data in working_hours_data:
            WorkingHour.objects.create(location=location, **wh_data)
        return location


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
    #average_rating = serializers.FloatField(source='get_average_rating', read_only=True)
    social_media = SocialMediaSerializer(many=True, read_only=True)
    # tags = serializers.CharField(source='get_tags_display', read_only=True)


    rating = serializers.SerializerMethodField()
    review_count = serializers.SerializerMethodField()

    def get_rating(self, obj):
        return round(obj.average_rating(), 1)  # Use the method defined in the model

    def get_review_count(self, obj):
        return obj.review_count()  # Call the review_count() method from the Service model

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
    user_name = serializers.CharField(source='user.username', read_only=True)

    def validate_rating(self, value):
        if value is None:
            raise serializers.ValidationError("Rating is required.")
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value

    class Meta:
        model = Review
        fields = ['id', 'rating', 'comment', 'created_at', 'user_name', 'user', 'service']
        read_only_fields = ['id', 'created_at', 'user', 'service']


        # fields = ['id', 'user_name', 'rating', 'comment', 'created_at']


# class ReviewSerializer(serializers.ModelSerializer):
#     user = serializers.StringRelatedField(read_only=True)

#     class Meta:
#         model = Review
#         fields = ['id', 'user', 'rating', 'comment', 'created_at']

