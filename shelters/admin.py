from django.contrib import admin
from .models import Shelter
# Register your models here.
# admin.site.register(Shelter)

@admin.register(Shelter)
class ShelterAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'city', 'street', 'postal_code', 'latitude', 'longitude')
    list_filter = ('country', 'region', 'city')
    search_fields = ('name', 'city', 'street', 'postal_code')


#admin.site.register(SocialMedia)  # Make sure this is registered if you want to add/edit social media entries