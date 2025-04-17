# Create your models here.
# services/models.py
from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import Avg
# from .models import SocialMedia

User = get_user_model()
    
class Service(models.Model):
    SERVICE_CATEGORIES = [
        (1, 'Dzīvnieku pieskatīšana'),         # Pet Sitting
        (2, 'Suņu pastaigas'),                # Dog Walking
        (3, 'Kopšana'),                       # Grooming
        (4, 'Apmācība'),                      # Training
        (5, 'Izmitināšana'),                  # Boarding
        (6, 'Veterinārārsts'),                # Veterinary
        (7, 'Foto sesijas'),                  # Pet Photography
        (8, 'Glābšana un meklēšana'),         # Pet Rescue and Search
        (9, 'Piederumi un aksesuāri'),        # Pet Supplies and Accessories
        (10, 'Māksla'),                       # Pet Art
        (11, 'Apbedīšana'),                   # Pet Burial Services
        (12, 'Transports'),                   # Pet Transportation
        (13, 'Audzētavas'),                   # Pet Breeders
        (14, 'Apdrošināšana'),                # Pet Insurance
        (15, 'Citi pakalpojumi'),             # Miscellaneous
    ]
    PROVIDER_TYPES = [
        (1, 'Fiziska persona'),    # Physical Person
        (2, 'Juridiska persona'),     # Legal Entity (Company)
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='services')
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.IntegerField(choices=SERVICE_CATEGORIES)
    created_at = models.DateTimeField(auto_now_add=True)

    # 🆕 Suggested fields:
    is_active = models.BooleanField(default=True)  # Allows soft-deactivation
    is_available = models.BooleanField(default=True, help_text="Is this service currently accepting requests?")
    # provider_type = models.CharField(max_length=20, choices=PROVIDER_TYPES, default='individual')
    provider_type = models.IntegerField(choices=PROVIDER_TYPES)
    service_image = models.URLField(max_length=255, null=False, blank=False, verbose_name="Servisa attēls")
    duration = models.DurationField(null=True, blank=True)  # For fixed service durations (e.g. 1h walk)
    #tags = models.CharField(max_length=255, blank=True)  # Comma-separated or for future tagging logic
    #rating = models.FloatField(default=0, help_text="Average rating")  # If you plan to allow reviews
    price_per_hour = models.DecimalField(max_digits=10, decimal_places=2)
    price_min = models.DecimalField(max_digits=10, decimal_places=2)  # Min price for different service packages
    price_max = models.DecimalField(max_digits=10, decimal_places=2)  # Max price for different service packages
    #review_count = models.PositiveIntegerField(default=0)  # To show how many reviews
    #language = models.CharField(max_length=10, default='lv')  # If you plan for multilingual
    website = models.URLField(blank=True, null=True, verbose_name="Vietne")
    # social_media = models.ManyToManyField(SocialMedia, blank=True, related_name='shelters', verbose_name="Sociālie mediji")

    def get_average_rating(self):
        # Calculate the average rating for this service
        avg_rating = self.reviews.aggregate(Avg('rating'))['rating__avg']
        return avg_rating or 0  # Return 0 if no reviews exist

    def __str__(self):
        return self.title
    




class Location(models.Model):
    PHONE_CODE_CHOICES = [
        ('+371', 'Latvija (+371)'),
        ('+370', 'Lietuva (+370)'),
        ('+372', 'Igaunija (+372)'),
    ]

    COUNTRY_CHOICES = [
        ('LV', 'Latvija'),
        ('EE', 'Igaunija'),
        ('LT', 'Lietuva'),
    ]

    service = models.ForeignKey(Service, related_name='locations', on_delete=models.CASCADE)
    # price = models.DecimalField(max_digits=10, decimal_places=2)
    # city = models.CharField(max_length=255)
    # address = models.TextField()
    country = models.CharField(max_length=2, choices=COUNTRY_CHOICES, blank=True, null=True, verbose_name="Valsts")



    region = models.CharField(max_length=100, blank=True, null=True, verbose_name="Reģions")  # State/Province
    city = models.CharField(max_length=100, blank=True, null=True, verbose_name="Pilsēta")
    street = models.CharField(max_length=200, blank=True, null=True, verbose_name="Iela")
    postal_code = models.CharField(max_length=20, blank=True, null=True, verbose_name="Pasta indekss")
    full_address = models.TextField(blank=True, null=True, verbose_name="Adrese")  # Optional, for storing formatted address

    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True, verbose_name="Ģeogrāfiskais platums")
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True, verbose_name="Ģeogrāfiskais garums")
    #phone_number = models.CharField(max_length=15, null=True, blank=True)
    #email = models.EmailField(null=True, blank=True)
    
    phone_number = models.CharField(max_length=15, blank=True, null=True, verbose_name="Telefona numurs")
    phone_code = models.CharField(max_length=5, null=True, blank=True, choices=PHONE_CODE_CHOICES, verbose_name="Telefona kods")
    email = models.EmailField(blank=True, null=True, verbose_name="E-pasts")

    def formatted_phone_code(self):
        return f"+{self.phone_code}" if self.phone_code else ""

    def __str__(self):
        return f'{self.service.title} - {self.city}'


class WorkingHour(models.Model):
    DAYS_OF_WEEK = [
        (0, 'Pirmdiena'), # Monday
        (1, 'Otrdiena'), # Tuesday
        (2, 'Trešdiena'), # Wednesday
        (3, 'Ceturtdiena'), # Thursday
        (4, 'Piektdiena'), # Friday
        (5, 'Sestdiena'), # Saturday
        (6, 'Svētdiena'), # Sunday
    ]

    location = models.ForeignKey(Location, related_name='working_hours', on_delete=models.CASCADE)
    day = models.IntegerField(choices=DAYS_OF_WEEK)
    from_hour = models.TimeField()
    to_hour = models.TimeField()

    class Meta:
        unique_together = ('location', 'day')
        ordering = ['day']

    def __str__(self):
        return f'{self.location.city} - {self.get_day_display()}: {self.from_hour}–{self.to_hour}'


class Review(models.Model):
    service = models.ForeignKey(Service, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)])  # 1-5 stars
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=True)

    class Meta:
        unique_together = ('service', 'user')
