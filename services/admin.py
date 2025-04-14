

from django.contrib import admin
from .models import Service, Location

# Define an inline for locations to be displayed within a Service entry
class LocationInline(admin.TabularInline):
    model = Location
    extra = 1  # Add extra empty form to add new locations directly from the service page

# Define the ServiceAdmin to customize how the Service model is displayed
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'price', 'created_at')  # Columns to display in the list view
    search_fields = ('title', 'category')  # Add search functionality
    list_filter = ('category',)  # Add a filter for categories in the sidebar
    inlines = [LocationInline]  # Show locations inline within the Service admin page

# Register the models in the admin panel
admin.site.register(Service, ServiceAdmin)
admin.site.register(Location)