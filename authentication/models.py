# Create your models here.
from django.contrib.auth.models import AbstractUser, Group, Permission, BaseUserManager
from django.db import models
import uuid
from django.utils import timezone
from datetime import timedelta

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        """
        Creates and returns a superuser with an email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_verified', True)  # Automatically verify superuser
        extra_fields.setdefault('is_active', True)    # Automatically activate superuser

        # Automatically generate a username if not provided
        if not extra_fields.get('username'):
            extra_fields['username'] = f"superuser_{uuid.uuid4().hex[:6]}"  # Or use your custom username generator

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    username = models.CharField(max_length=255, unique=True, blank=True)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=False)  # Prevent login until verified
    is_verified = models.BooleanField(default=False)  # Tracks if email is verified

    # Field to store the animal for the avatar
    avatar_animal = models.CharField(max_length=100, blank=True, null=True, default="Cat")  # Animal name for avatar

    # Email Verification
    activation_token = models.CharField(max_length=100, blank=True, null=True)
    activation_token_expires = models.DateTimeField(blank=True, null=True)

    # Password Reset
    password_reset_token = models.CharField(max_length=100, blank=True, null=True)  # Reset token
    password_reset_expires = models.DateTimeField(blank=True, null=True)  # Expiry for reset

    objects = CustomUserManager()  # Use the custom manager

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

            # Automatically generate a username if not provided
            if not self.username:
                self.username = f"user_{uuid.uuid4().hex[:8]}"

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
