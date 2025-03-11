from django.contrib import admin
from .models import Pet, PetSightingHistory, UserFavorites
# Register your models here.


# class PetAdmin(admin.ModelAdmin):
#     list_display = ('name', 'image_tag', 'image')  # Add 'image_tag' to list_display

#     # Optionally, you can add custom image preview in the form view as well
#     fields = ('name', 'image', 'image_tag')  # Display image and the tag in the form vi

# Register your models here
# admin.site.register(Pet)
# admin.site.register(PetStatusHistory)
admin.site.register(PetSightingHistory)
admin.site.register(UserFavorites)

@admin.register(Pet)
class ShelterAdmin(admin.ModelAdmin):
    # list_display = ('name', 'size', 'species', 'gender')
    list_display = ('size', 'species', 'gender')
    list_filter = ('species', 'gender')
    search_fields = ('species', 'gender', 'size')


# class PetAdmin(admin.ModelAdmin):
#     list_display = ('name', 'size', 'gender', 'behavior', 'identifier')  # Fields to display in list view
#     search_fields = ('name', 'identifier')  # Make the `name` and `identifier` fields searchable
#     list_filter = ('size', 'gender', 'behavior')  # Add filters for `size`, `gender`, and `behavior`

# admin.site.register(Pet, PetAdmin)