from django.db import models
from core.models import SocialMedia
# Create your models here.
from django.contrib.postgres.fields import ArrayField  # If you use PostgreSQL, otherwise JSONField is recommended

class Shelter(models.Model):

    # Define predefined choices for phone codes
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

    name = models.CharField(max_length=200, verbose_name="Nosaukums")
    description = models.TextField(blank=True, null=True, verbose_name="Apraksts")
    website = models.URLField(blank=True, null=True, verbose_name="Vietne")

    # Use predefined choices for the country field
    country = models.CharField(max_length=2, choices=COUNTRY_CHOICES, blank=True, null=True, verbose_name="Valsts")



    region = models.CharField(max_length=100, blank=True, null=True, verbose_name="Reģions")  # State/Province
    city = models.CharField(max_length=100, blank=True, null=True, verbose_name="Pilsēta")
    street = models.CharField(max_length=200, blank=True, null=True, verbose_name="Iela")
    postal_code = models.CharField(max_length=20, blank=True, null=True, verbose_name="Pasta indekss")
    full_address = models.TextField(blank=True, null=True, verbose_name="Adrese")  # Optional, for storing formatted address

    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True, verbose_name="Ģeogrāfiskais platums")
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True, verbose_name="Ģeogrāfiskais garums")

     # Social Media
    #social_media = models.ManyToManyField(SocialMedia, blank=True, related_name='shelters', verbose_name="Sociālie mediji")
    #social_media = models.JSONField(default=list, blank=True, verbose_name="Sociālie mediji")
    # Social Media: Multiple social media platforms can be chosen
    social_media = models.ManyToManyField(SocialMedia, blank=True, related_name='shelters', verbose_name="Sociālie mediji")

    phone_number = models.CharField(max_length=15, blank=True, null=True, verbose_name="Telefona numurs")
    phone_code = models.CharField(max_length=5, null=True, blank=True, choices=PHONE_CODE_CHOICES, verbose_name="Telefona kods")

    email = models.EmailField(blank=True, null=True, verbose_name="E-pasts")

    def formatted_phone_code(self):
        return f"+{self.phone_code}" if self.phone_code else ""

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        #Automatically generate full address if all components are present
        if all([self.street, self.city, self.country]):
            self.full_address = f"{self.street}, {self.city}, {self.region or ''}, {self.country} - {self.postal_code or ''}".strip(', -')
        super().save(*args, **kwargs)
