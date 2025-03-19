# from django.db import models

# # Create your models here.
# from django.contrib.auth.models import User
# from django.db import models

# class UserProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
#     language = models.CharField(max_length=10, default="en")

#     def __str__(self):
#         return f"{self.user.username} Profile"

# from django.contrib.auth.models import AbstractUser
# from django.db import models

# class CustomUser(AbstractUser):
#     email = models.EmailField(unique=True)  # ✅ Ensures no two users can have the same email


# from django.contrib.auth.models import AbstractUser
# from django.db import models

# class CustomUser(AbstractUser):
#     email = models.EmailField(unique=True)  # ✅ Make email unique

    # USERNAME_FIELD = "email"  # ✅ Use email for authentication instead of username
    # REQUIRED_FIELDS = []  # Remove username requirement

# from django.contrib.auth.models import AbstractUser
# from django.db import models
# import uuid
# from django.utils import timezone
# from datetime import timedelta

# class CustomUser(AbstractUser):
#     username = models.CharField(max_length=255, unique=True, blank=True)  # ✅ Auto-generated username
#     email = models.EmailField(unique=True)
#     is_active = models.BooleanField(default=False)  # ❌ Prevents login until verified
#     is_verified = models.BooleanField(default=False)  # ❌ Tracks if email is verified

#     # Email Verification
#     activation_token = models.CharField(max_length=100, blank=True, null=True)
#     activation_token_expires = models.DateTimeField(blank=True, null=True)

#     # Password Reset
#     password_reset_token = models.CharField(max_length=100, blank=True, null=True)  # ✅ Reset token
#     password_reset_expires = models.DateTimeField(blank=True, null=True)  # ✅ Expiry for reset

#     USERNAME_FIELD = "email"
#     REQUIRED_FIELDS = []  # ✅ No username required for Django superusers

#     def save(self, *args, **kwargs):
#         """Generate activation token and expiry date only on user creation."""
#         if self.pk is None:  # ✅ Only generate token when user is first created
#             self.activation_token = str(uuid.uuid4())
#             self.activation_token_expires = timezone.now() + timedelta(hours=24)  # ✅ Use timezone-aware timestamps

#             if not self.username:  # ✅ Auto-generate username if missing
#                 self.username = self.generate_unique_username()

#         super().save(*args, **kwargs)

#     def generate_unique_username(self):
#         """Generate a random, unique username."""
#         return f"user_{uuid.uuid4().hex[:12]}"  # ✅ Simple unique username

#     def generate_password_reset_token(self):
#         """Generate a password reset token with expiry."""
#         self.password_reset_token = str(uuid.uuid4())
#         self.password_reset_expires = timezone.now() + timedelta(hours=1)  # ✅ Use timezone-aware timestamps
#         self.save()

#     def clear_password_reset_token(self):
#         """Remove password reset token after use."""
#         self.password_reset_token = None
#         self.password_reset_expires = None
#         self.save()

#     def __str__(self):
#         return self.email

from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
import uuid
from django.utils import timezone
from datetime import timedelta

class CustomUser(AbstractUser):
    username = models.CharField(max_length=255, unique=True, blank=True)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=False)  # Prevent login until verified
    is_verified = models.BooleanField(default=False)  # Tracks if email is verified

    # Email Verification
    activation_token = models.CharField(max_length=100, blank=True, null=True)
    activation_token_expires = models.DateTimeField(blank=True, null=True)

    # Password Reset
    password_reset_token = models.CharField(max_length=100, blank=True, null=True)  # Reset token
    password_reset_expires = models.DateTimeField(blank=True, null=True)  # Expiry for reset

    # ✅ Fix Reverse Accessor Errors
    groups = models.ManyToManyField(Group, related_name="customuser_set", blank=True)  
    user_permissions = models.ManyToManyField(Permission, related_name="customuser_permissions_set", blank=True)  

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def save(self, *args, **kwargs):
        """Generate activation token and expiry date only on user creation."""
        if self.pk is None:  # Only generate token when user is first created
            self.activation_token = str(uuid.uuid4())
            self.activation_token_expires = timezone.now() + timedelta(hours=24)

            if not self.username:  # Auto-generate username if missing
                self.username = self.generate_unique_username()

        super().save(*args, **kwargs)

    def generate_unique_username(self):
        """Generate a random, unique username."""
        return f"user_{uuid.uuid4().hex[:12]}"

    def generate_password_reset_token(self):
        """Generate a password reset token with expiry."""
        self.password_reset_token = str(uuid.uuid4())
        self.password_reset_expires = timezone.now() + timedelta(hours=1)
        self.save()

    def clear_password_reset_token(self):
        """Remove password reset token after use."""
        self.password_reset_token = None
        self.password_reset_expires = None
        self.save()

    def __str__(self):
        return self.email
