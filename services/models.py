from django.db import models

# Create your models here.
# services/models.py


class Service(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=100)  # e.g. Dog Walking, Pet Sitting, etc.
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class Location(models.Model):
    service = models.ForeignKey(Service, related_name='locations', on_delete=models.CASCADE)
    city = models.CharField(max_length=255)
    address = models.TextField()
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)

    def __str__(self):
        return f'{self.service.title} - {self.city}'
