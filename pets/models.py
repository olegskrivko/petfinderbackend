from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db import models

class Pet(models.Model):
    SIZE_CHOICES = [
        (1, 'Mazs'), # Small
        (2, 'Vidējs'), # Medium
        (3, 'Liels'), # Large
    ]
    GENDER_CHOICES = [
        (1, 'Tēviņš'), # Male
        (2, 'Mātīte'), # Female
    ]
    BEHAVIOR_CHOICES = [
        (1, 'Draudzīgs'), # Friendly  
        (2, 'Agresīvs'), # Aggressive
        (3, 'Mierīgs'), # Calm
        (4, 'Bailīgs'), # Fearful
        (5, 'Paklausīgs'), # Obedient
    ]
    SPECIES_CHOICES = [
        (1, 'Suns'), # Dog
        (2, 'Kaķis'), # Cat
        (3, 'Cits'), # Other
    ]
    AGE_CHOICES = [
        (1, 'Mazulis'), # Young
        (2, 'Pieaugušais'), # Adult
        (3, 'Seniors'), # Senior
    ]
    PATTERN_CHOICES = [
        (1, 'Vienkrāsains'), # Solid
        (2, 'Strīpains'), # Striped
        (3, 'Punktveida'), # Spotted
        (4, 'Plankumains'), # Patched
        (5, 'Raibs'), # Marbled
    ]
    COLOR_CHOICES = [
        (1, 'Melns'), # Black
        (2, 'Pelēks'), # Gray
        (3, 'Balts'), # White
        (4, 'Krēmīgs'), # Cream
        (5, 'Dzeltens'), # Yellow
        (6, 'Zeltains'), # Golden
        (7, 'Brūns'), # Brown
        (8, 'Sarkans'), # Red
        (9, 'Lillīgs'), # Lilac
        (10, 'Zils'), # Blue
        (11, 'Zaļš'), # Green
        (12, 'Haki'), # Khaki
        (13, 'Bēšīgs'), # Beige
        (14, 'Dzeltenbrūns'), # Fawn
        (15, 'Kaštanbrūns'), # Chestnut
    ]
    PHONE_CODE_CHOICES = [
        (371, 'LV (+371)'), # Latvia
        (370, 'LT (+370)'), # Lithuania
        (372, 'EE (+372)'), # Estonia
    ]
    # Name of the pet is optional
    name = models.CharField(max_length=100, blank=True, null=True, verbose_name="Vārds")
    # Identifier is optional
    identifier = models.CharField(max_length=100, blank=True, null=True, verbose_name="ID")
    # Behavior is optional
    behavior = models.IntegerField(choices=BEHAVIOR_CHOICES, blank=True, null=True, verbose_name="Uzvedība")
    # Size is optional  
    size = models.IntegerField(choices=SIZE_CHOICES, blank=True, null=True, verbose_name="Izmērs")
    # Age is optional  
    age = models.IntegerField(choices=AGE_CHOICES, blank=True, null=True, verbose_name="Vecums")
    # Gender is optional
    gender = models.IntegerField(choices=GENDER_CHOICES, blank=True, null=True, verbose_name="Dzimums")
    # Species is required
    species = models.IntegerField(choices=SPECIES_CHOICES, blank=False, null=False, verbose_name="Suga")
    # Pattern is optional
    pattern = models.IntegerField(choices=PATTERN_CHOICES, blank=True, null=True, verbose_name="Kažoka raksts")
    # Primary color is optional
    primary_color = models.IntegerField(choices=COLOR_CHOICES, blank=True, null=True, verbose_name="Pamatkrāsa")
    # Secondary color is optional
    secondary_color = models.IntegerField(choices=COLOR_CHOICES, blank=True, null=True, verbose_name="Sekundārā krāsa")
    # Optional: Additional notes or information about the sighting
    notes = models.TextField(blank=True, null=True, verbose_name="Piezīmes")
    # Timestamp for when the entry is created
    created_at = models.DateTimeField(auto_now_add=True, null=True)  # Automatically set the current date and time when a new pet is added
    # Post author is required
    #author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pets', verbose_name="Autors") # Allows reverse lookup using user.pets.all()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # ✅ Fix here
    # Post author contact phone number is optional
    contact_phone = models.IntegerField(blank=True, null=True, verbose_name="Kontakttālrunis")
    # Phone code is optional  
    phone_code = models.IntegerField(choices=PHONE_CODE_CHOICES, blank=True, null=True, verbose_name="Telefona kods")
    # Breed is optional 
    breed = models.CharField(max_length=100, blank=True, null=True, verbose_name="Sķirne")

    #is_published = models.BooleanField()
    #is_closed = models.BooleanField()

    # Add an image field for pet photos
    image = models.ImageField(upload_to='pet_images/', blank=True, null=True, verbose_name="Attēls")
    
    extra_image_1 = models.ImageField(upload_to='pet_images/', blank=True, null=True, verbose_name="Papildus attēls 1.")
    extra_image_2 = models.ImageField(upload_to='pet_images/', blank=True, null=True, verbose_name="Papildus attēls 2.")
    extra_image_3 = models.ImageField(upload_to='pet_images/', blank=True, null=True, verbose_name="Papildus attēls 3.")
    extra_image_4 = models.ImageField(upload_to='pet_images/', blank=True, null=True, verbose_name="Papildus attēls 4.")

    # class Meta:
    #     verbose_name = "Pet"
    #     verbose_name_plural = "Pets"

    # def __str__(self):
    #     return self.name

    def __str__(self):
        return self.name if self.name else f"Pet ID {self.id}"  # Ensures __str__ always returns a string
    
    class Meta:
        #db_table = 'Mājdzīvnieki'  # Custom table name
        verbose_name = "Mājdzīvnieks"  # Singular name in the admin
        verbose_name_plural = "Mājdzīvnieki"  # Plural name in the admin
    
    # def image_tag(self):
    #     if self.image:
    #         return f'<img src="{self.image.url}" width="50" height="50" />'
    #     return "No image"
    # image_tag.short_description = 'Image'
    # image_tag.allow_tags = True  # Allow HTML tags for image rendering

class PetSightingHistory(models.Model):
    pet = models.ForeignKey('Pet', on_delete=models.CASCADE, related_name='sightings_history')
    # Location where the pet was sighted (latitude and longitude)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    # Timestamp of when the sighting occurred
    timestamp = models.DateTimeField(auto_now_add=True, null=True)
    # User who reported the sighting
    #reporter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reported_sightings')
    reporter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # ✅ Fix here
    # Optional: Additional notes or information about the sighting
    notes = models.TextField(blank=True, null=True)
    #is_closed = models.BooleanField()
    #comment_success_story_or_not
    # Add an image field for pet photos
    image = models.ImageField(upload_to='sightnings_images/', blank=True, null=True, verbose_name="Attēls")
    #is_dead/blurred/sensitive
    STATUS_CHOICES = [
        (1, 'Pazudis'), # Lost
        (2, 'Atrasts'), # Found
        (3, 'Redzēts'), # Seen
    ]

    # ForeignKey to Pet model to link status history to a pet
    #pet = models.ForeignKey('Pet', on_delete=models.CASCADE, related_name='status_history')
    # Status of the pet (Lost, Found, Seen)
    status = models.IntegerField(choices=STATUS_CHOICES, verbose_name="Statuss")
    # Timestamp of when the status changed
    #timestamp = models.DateTimeField(auto_now_add=True, null=True)
    # Date and time when the event (lost, found, or seen) occurred
    event_occurred_at = models.DateTimeField(blank=True, null=True, verbose_name="Notikuma laiks")  # Event time (Lost, Found, Seen)
    class Meta:
        ordering = ['-timestamp']  # Newest status changes first. Change to 'timestamp' for oldest first.

    def __str__(self):
        return f"{self.pet.name} - {self.get_status_display()} at {self.timestamp}"



class UserFavorites(models.Model):
    #user = models.ForeignKey(User, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # ✅ Fix here
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'pet')  # Ensure each user can only add a pet once

    def __str__(self):
        return f"{self.user.username} - {self.pet.name}"
