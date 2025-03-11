from django.db import models

# Create your models here.
# core/models.py

from django.db import models

# class Country(models.Model):
#     # Name of the country
#     name = models.CharField(max_length=255)
#     # ISO 3166-1 alpha-2 country code (2-letter country code)
#     country_code = models.CharField(max_length=2, unique=True)  # e.g., 'LV' for Latvia, 'EE' for Estonia
#     # Capital city of the country
#     capital = models.CharField(max_length=255, blank=True, null=True)
#     # ISO 4217 3-letter currency code (e.g., 'EUR' for Euro)
#     currency = models.CharField(max_length=3, blank=True, null=True)  # e.g., EUR, USD
#     # ISO 639-1 2-letter language code (e.g., 'lv' for Latvian, 'et' for Estonian)
#     language = models.CharField(max_length=2, blank=True, null=True)  # e.g., lv, et
#     # International phone code (e.g., +1, +44)
#     phone_code = models.CharField(max_length=5)  # e.g., +44 for UK, +1 for USA
    
#     def __str__(self):
#         return self.name

    
class SocialMedia(models.Model):
    # Defining the available platforms as a set of choices
    PLATFORM_CHOICES = [
        (1, 'Facebook'),
        (2, 'Instagram'),
        (3, 'X'),
        (4, 'LinkedIn'),
        (5, 'YouTube'),
        (6, 'TikTok'),
        (7, 'Pinterest'),
        (8, 'Snapchat'),
    ]
    platform = models.IntegerField(choices=PLATFORM_CHOICES, blank=False, null=False, verbose_name="Platforma")
    profile_url = models.URLField()  # URL of the profile
    is_official = models.BooleanField(default=False)  # Whether it's an official profile (e.g., government, embassy)
    is_verified = models.BooleanField(default=False)  # Whether the profile is verified (default to False)

    def __str__(self):
        return dict(self.PLATFORM_CHOICES).get(self.platform, "Unknown Platform")
