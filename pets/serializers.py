# pets/serializers.py
#from django.contrib.auth.models import User 
from rest_framework import serializers
from .models import Pet, PetSightingHistory
from django.utils import timezone
from django.contrib.auth import get_user_model
User = get_user_model()
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']  # Include fields you want to display

class PetSightingHistorySerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display')
    status = serializers.IntegerField()  # This ensures you return the raw integer value, not the display string
    reporter = UserSerializer(read_only=True)  # Serialize the User field
    #reporter = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)  # Make reporter writable (User ID)
    #image = serializers.ImageField(required=False, allow_null=True)  # Handle image field (optional)  # Handle image field (optional)
    #image_url = serializers.SerializerMethodField()  # ✅ Fix: Use `SerializerMethodField`
    pet = serializers.PrimaryKeyRelatedField(queryset=Pet.objects.all())  # ✅ Ensure `pet` exists
    event_occurred_at = serializers.DateTimeField(required=False, allow_null=True)  # ✅ Ensure it's an aware datetime
    class Meta:
        model = PetSightingHistory
        fields = '__all__' 
        #fields = ['latitude', 'longitude', 'timestamp', 'reporter', 'notes', 'status', 'image', 'event_occurred_at']  # Add the fields you want to include

    # def get_image_url(self, obj):
    #     print("self",self)
    #     """ ✅ Return Cloudinary Image URL for sightings """
    #     return obj.image if obj.image else None

    def validate(self, data):
        # Check if latitude and longitude are provided and are valid
        """Ensure latitude and longitude are valid."""
        latitude = data.get('latitude')
        longitude = data.get('longitude')

        if not latitude or not longitude:
            raise serializers.ValidationError("Latitude and longitude must be provided.")
        
        try:
            latitude = float(latitude)
            longitude = float(longitude)
        except ValueError:
            raise serializers.ValidationError("Latitude and longitude must be valid numbers.")

        # Optionally, check for valid ranges
        if not (-90 <= latitude <= 90):
            raise serializers.ValidationError("Latitude must be between -90 and 90 degrees.")
        if not (-180 <= longitude <= 180):
            raise serializers.ValidationError("Longitude must be between -180 and 180 degrees.")
        
        return data
# class PetStatusHistorySerializer(serializers.ModelSerializer):
#     # This will use the display value from STATUS_CHOICES, not just the integer.
#     status = serializers.CharField(source='get_status_display')

#     class Meta:
#         model = PetStatusHistory
#         fields = ['status', 'timestamp', 'event_occurred_at']  # You can add more fields if needed

class PetSerializer(serializers.ModelSerializer):
    size_display = serializers.CharField(source='get_size_display', read_only=True)
    contact_phone_display = serializers.CharField(source='get_contact_phone_display', read_only=True)
    gender_display = serializers.CharField(source='get_gender_display', read_only=True)
    species_display = serializers.CharField(source='get_species_display', read_only=True)
    behavior_display = serializers.CharField(source='get_behavior_display', read_only=True)
    age_display = serializers.CharField(source='get_age_display', read_only=True)
    pattern_display = serializers.CharField(source='get_pattern_display', read_only=True)
    primary_color_display = serializers.CharField(source='get_primary_color_display', read_only=True)
    secondary_color_display = serializers.CharField(source='get_secondary_color_display', read_only=True)
    notes_display = serializers.CharField(source='get_notes_display', read_only=True)
    pet_image = serializers.CharField(required=False, allow_blank=True)  # ✅ Accepts empty values
    # image_url = serializers.SerializerMethodField()
    # extra_image_1_url = serializers.SerializerMethodField()
    # extra_image_2_url = serializers.SerializerMethodField()
    # extra_image_3_url = serializers.SerializerMethodField()
    # extra_image_4_url = serializers.SerializerMethodField()

    # image = serializers.ImageField(required=False, allow_null=True)  # ✅ Fix: Allow empty image
    # extra_image_1 = serializers.ImageField(required=False, allow_null=True)
    # extra_image_2 = serializers.ImageField(required=False, allow_null=True)
    # extra_image_3 = serializers.ImageField(required=False, allow_null=True)
    # extra_image_4 = serializers.ImageField(required=False, allow_null=True)

    author = UserSerializer(read_only=True)  # Add the UserSerializer here
    
    sightings_history = PetSightingHistorySerializer(many=True, read_only=True)  # Include related sighting history

    #status_history = PetSightingHistorySerializer(many=True, read_only=True)
     # ✅ Accept `latitude`, `longitude`, and `status` as writeable fields (for the first sighting)
    latitude = serializers.DecimalField(max_digits=9, decimal_places=6, write_only=True, required=True)
    longitude = serializers.DecimalField(max_digits=9, decimal_places=6, write_only=True, required=True)
    status = serializers.IntegerField(write_only=True, required=True)
     # This will return the human-readable value for the status
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Pet
        #fields = ['id', 'name']
        fields = '__all__'  # Include all fields from the model

    # ✅ Fix Cloudinary Image URLs
    # def get_image_url(self, obj):
    #     return obj.image  # Directly return stored URL

    # def get_extra_image_1_url(self, obj):
    #     return obj.extra_image_1 if obj.extra_image_1 else None

    # def get_extra_image_2_url(self, obj):
    #     return obj.extra_image_2 if obj.extra_image_2 else None

    # def get_extra_image_3_url(self, obj):
    #     return obj.extra_image_3 if obj.extra_image_3 else None

    # def get_extra_image_4_url(self, obj):
    #     return obj.extra_image_4 if obj.extra_image_4 else None

    # def get_image_url(self, obj):
    #     """ ✅ Return Cloudinary Image URL """
    #     return obj.image if obj.image else None
    
    # def create(self, validated_data):
    #     """ ✅ Create only the Pet (No PetSightingHistory is created here). """
    #     return Pet.objects.create(**validated_data)  # No sighting creation here
    def create(self, validated_data):
        print("🔥 PetSerializer.create() hit!")  # Debugging Line
        """
        ✅ Create only the Pet (No PetSightingHistory is created here).
        """
        # 🔴 Remove extra fields before creating a Pet
        validated_data.pop('latitude', None)
        validated_data.pop('longitude', None)
        validated_data.pop('status', None)

        # return Pet.objects.create(**validated_data)
        pet = Pet.objects.create(**validated_data)
        print(f"✅ Pet {pet.id} saved successfully!")  # Debugging
        return pet
    # def create(self, validated_data):
    #     """
    #     ✅ Create a Pet and automatically create a PetSightingHistory entry.
    #     """
    #     latitude = validated_data.pop('latitude')
    #     longitude = validated_data.pop('longitude')
    #     status = validated_data.pop('status')
    #     user = self.context['request'].user  # Get the authenticated user
    #     # Remove 'author' here because it is assigned in perform_create
    #     # ✅ Create the pet
    #     # pet = Pet.objects.create(**validated_data, author=user)
    #     pet = Pet.objects.create(**validated_data)

    #     # ✅ Create the first sighting history entry
    #     PetSightingHistory.objects.create(
    #         pet=pet,
    #         latitude=latitude,
    #         longitude=longitude,
    #         status=status,
    #         reporter=user,
    #         event_occurred_at=timezone.now()
    #     )

    #     return pet

