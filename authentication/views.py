from django.core.mail import send_mail
from django.utils.timezone import now
from django.conf import settings
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import os
import uuid
from datetime import datetime, timedelta
from .serializers import RegisterSerializer, LoginSerializer, ForgotPasswordSerializer, ResetPasswordSerializer
User = get_user_model()

DOMAIN_APP_URL = os.getenv("DOMAIN_APP_URL")

@api_view(["GET"])
@permission_classes([AllowAny])  # ✅ Make activation public
def activate_user(request, token):
    """Activate the user if the token is valid and not expired."""
    user = get_object_or_404(User, activation_token=token)

    # ✅ Check if the account is already active
    if user.is_active:
        return Response({"message": "Account is already verified!"}, status=status.HTTP_400_BAD_REQUEST)

    # ✅ Check if the activation token is expired
    if user.activation_token_expires and user.activation_token_expires < now():
        return Response({"error": "Activation link has expired."}, status=status.HTTP_400_BAD_REQUEST)

    # ✅ Activate the user
    user.is_active = True
    user.is_verified = True  # If you are using a separate `is_verified` field
    user.activation_token = None  # ✅ Remove the token
    user.activation_token_expires = None  # ✅ Clear expiry
    user.save()

    # ✅ Redirect to React frontend login page instead of Django
    return redirect(f"{DOMAIN_APP_URL}/login")  # Change to your React frontend URL

    #return redirect("/login")  # ✅ Redirect user to login page after activation
# @api_view(["GET"])
# def activate_user(request, token):
#     """Activate the user if the token is valid."""
#     try:
#         user = User.objects.get(activation_token=token, activation_token_expires__gt=now())
#         if user.is_active:
#             return Response({"message": "Account is already verified!"}, status=status.HTTP_400_BAD_REQUEST)

#         user.is_active = True
#         user.activation_token = None  # ✅ Remove the token after activation
#         user.activation_token_expires = None
#         user.save()

#         return redirect("/login")  # ✅ Redirects to login page in React

#     except User.DoesNotExist:
#         return Response({"error": "Invalid or expired activation link."}, status=status.HTTP_400_BAD_REQUEST)

# @api_view(["GET"])
# def activate_user(request, token):
#     """Activates user if the token is valid and not expired."""
#     user = get_object_or_404(User, activation_token=token)

#     if user.is_active:
#         return Response({"message": "Account is already verified!"}, status=status.HTTP_400_BAD_REQUEST)

#     user.is_active = True  # ✅ Allows login
#     user.is_verified = True  # ✅ Marks email as verified
#     user.activation_token = None  # ✅ Remove token after activation
#     user.activation_token_expires = None  # ✅ Clear expiry date
#     user.save()

#     return Response({"message": "Account activated successfully!"}, status=status.HTTP_200_OK)
### ✅ Forgot Password View (Request Reset Link)
@api_view(["POST"])
@permission_classes([AllowAny])
def reset_password(request, token):  # ✅ Token must match URLs
    print("token", token)
    """Handles password reset using a valid token."""
    try:
        user = User.objects.get(password_reset_token=token)
    except User.DoesNotExist:
        return Response({"error": "Invalid or expired token."}, status=400)

    # ✅ Check if token is expired
    if user.password_reset_expires and user.password_reset_expires < now():
        return Response({"error": "Password reset link has expired."}, status=400)

    # ✅ Update password
    new_password = request.data.get("password")
    if not new_password:
        return Response({"error": "Password is required."}, status=400)

    user.set_password(new_password)
    user.password_reset_token = None  # ✅ Remove token after use
    user.password_reset_expires = None
    user.save()

    return Response({"message": "Password reset successfully! You can now log in."}, status=200)

# @api_view(["POST"])
# @permission_classes([AllowAny])
# def reset_password(request, token):
#     """Handles password reset using a valid token."""
#     try:
#         user = User.objects.get(password_reset_token=token)
#     except User.DoesNotExist:
#         return Response({"error": "Invalid or expired token."}, status=400)

#     # ✅ Check if token is expired
#     if user.password_reset_expires and user.password_reset_expires < now():
#         return Response({"error": "Password reset link has expired."}, status=400)

#     # ✅ Update password
#     new_password = request.data.get("password")
#     if not new_password:
#         return Response({"error": "Password is required."}, status=400)

#     user.set_password(new_password)
#     user.password_reset_token = None  # Remove token after use
#     user.password_reset_expires = None
#     user.save()

#     return Response({"message": "Password reset successfully! You can now log in."}, status=200)

@api_view(["POST"])
@permission_classes([AllowAny])
def forgot_password(request):
    """Handles password reset requests by sending an email."""
    email = request.data.get("email")
    
    if not email:
        return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({"error": "No account found with this email."}, status=status.HTTP_404_NOT_FOUND)

    # ✅ Generate password reset token
    user.password_reset_token = str(uuid.uuid4())
    user.password_reset_expires = now() + timedelta(hours=1)  # Token expires in 1 hour
    user.save()

    # ✅ Create the reset link
    reset_url = f"{DOMAIN_APP_URL}/reset-password/{user.password_reset_token}/"

    # ✅ Render HTML email template
    context = {"reset_url": reset_url, "user": user}
    html_content = render_to_string("emails/reset_password.html", context)  # Load email template
    plain_text_content = strip_tags(html_content)  # Convert HTML to plain text

    # ✅ Send email
    subject = "Reset Your Password"
    email_message = EmailMultiAlternatives(subject, plain_text_content, settings.EMAIL_HOST_USER, [user.email])
    email_message.attach_alternative(html_content, "text/html")  # Attach HTML version
    email_message.send()

    return Response({"message": "Password reset email sent!"}, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([AllowAny])
def reset_password(request, token):
    """Handles password reset using a valid token."""
    data = request.data.copy()  # ✅ Copy request data
    data["token"] = token  # ✅ Add `token` from URL to data

    serializer = ResetPasswordSerializer(data=data)
    if serializer.is_valid():
        serializer.save()  # ✅ Calls `save()` and updates password
        return Response({"message": "Password reset successfully! You can now log in."}, status=200)
    
    return Response(serializer.errors, status=400)  # 🚨 Send back validation errors


### ✅ Register View (Create User & Send Verification Email)
@api_view(["POST"])
@permission_classes([AllowAny])
def register(request):
    """Handles user registration and sends a verification email."""
    serializer = RegisterSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.save()  # Serializer handles user creation & email sending
        return Response({
            "message": "User registered! Check your email to verify your account."
        }, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

### ✅ Login View (JWT)
@api_view(["POST"])
@permission_classes([AllowAny])
def login(request):
    """Handles user login with JWT authentication."""
    print("Received login request:", request.data)  # ✅ Debugging: Print request data
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data["user"]  # Extract user
        refresh = RefreshToken.for_user(user)  # Generate JWT tokens
        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "username": user.username,
            "avatar_animal": user.avatar_animal,
        }, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

### ✅ Get User Details (Authenticated Users Only)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_user_details(request):
    """Returns user details for authenticated users."""
    user = request.user
    return Response({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "avatar_animal": user.avatar_animal,
    }, status=status.HTTP_200_OK)

### ✅ Delete User View (Soft Delete Instead of Permanent Deletion)
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_user(request):
    """Soft deletes the user account (deactivates it)."""
    user = request.user
    user.is_active = False  # ✅ Instead of deleting, deactivate the account
    user.save()
    return Response({"message": "User account deactivated successfully."}, status=status.HTTP_204_NO_CONTENT)

### ✅ Logout View (Blacklist Token)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout(request):
    """Handles logout by blacklisting refresh token."""
    if "refresh" not in request.data:
        return Response({"error": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        refresh_token = request.data["refresh"]
        token = RefreshToken(refresh_token)
        token.blacklist()  # ✅ Blacklist the token
        return Response({"message": "Logout successful"}, status=status.HTTP_205_RESET_CONTENT)
    except Exception as e:
        return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)