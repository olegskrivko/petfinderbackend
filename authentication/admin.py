from django.contrib import admin

# Register your models here.
# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
# from django.contrib.auth.models import User
# from user_profile.models import UserProfile

# # Define an inline admin for UserProfile
# class UserProfileInline(admin.StackedInline):
#     model = UserProfile
#     can_delete = False
#     verbose_name_plural = "User Profile"
#     fields = ('language',)  # Display language field

# # Extend UserAdmin to include UserProfile
# class CustomUserAdmin(UserAdmin):
#     inlines = (UserProfileInline,)

# # Unregister default User admin and register the new one
# admin.site.unregister(User)
# admin.site.register(User, CustomUserAdmin)