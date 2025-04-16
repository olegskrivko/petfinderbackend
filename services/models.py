# Create your models here.
# services/models.py
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()
    
class Service(models.Model):
    SERVICE_CATEGORIES = [
        (1, 'Pet Sitting'),
        (2, 'Dog Walking'),
        (3, 'Grooming'),
        (4, 'Training'),
        (5, 'Boarding'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='services')
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.IntegerField(choices=SERVICE_CATEGORIES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    


class Location(models.Model):
    service = models.ForeignKey(Service, related_name='locations', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    city = models.CharField(max_length=255)
    address = models.TextField()
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

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

