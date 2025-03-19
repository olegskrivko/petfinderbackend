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
import uuid
from datetime import datetime, timedelta
from .serializers import RegisterSerializer, LoginSerializer, ForgotPasswordSerializer, ResetPasswordSerializer
User = get_user_model()

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
    return redirect("http://localhost:5173/login")  # Change to your React frontend URL

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
    reset_url = f"http://localhost:5173/reset-password/{user.password_reset_token}/"

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
###### CORECT
# @api_view(["POST"])
# @permission_classes([AllowAny])
# def forgot_password(request):
#     """Handles password reset requests by sending an email."""
#     email = request.data.get("email")
    
#     if not email:
#         return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)

#     try:
#         user = User.objects.get(email=email)
#     except User.DoesNotExist:
#         return Response({"error": "No account found with this email."}, status=status.HTTP_404_NOT_FOUND)

#     # ✅ Generate password reset token
#     user.password_reset_token = str(uuid.uuid4())
#     user.password_reset_expires = now() + timedelta(hours=1)  # Token expires in 1 hour
#     user.save()

#     # ✅ Send reset email
#     reset_url = f"http://localhost:5173/reset-password/{user.password_reset_token}/"  # Adjust frontend URL
#     subject = "Reset Your Password"
#     message = f"Click the link below to reset your password:\n\n{reset_url}"

#     send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])

#     return Response({"message": "Password reset email sent!"}, status=status.HTTP_200_OK)
# @api_view(["POST"])
# @permission_classes([AllowAny])
# def forgot_password(request):
#     """Handles password reset requests by sending an email."""
#     serializer = ForgotPasswordSerializer(data=request.data)
#     if serializer.is_valid():
#         return Response(serializer.save(), status=status.HTTP_200_OK)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

### ✅ Reset Password View (Submit New Password)
# @api_view(["POST"])
# @permission_classes([AllowAny])
# def reset_password(request):
#     """Handles password reset."""
#     serializer = ResetPasswordSerializer(data=request.data)
#     if serializer.is_valid():
#         return Response(serializer.save(), status=status.HTTP_200_OK)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     return Response({"message": "Password reset successfully!"}, status=status.HTTP_200_OK)

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

# from django.core.mail import send_mail
# from django.utils.timezone import now
# from rest_framework import status
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import AllowAny, IsAuthenticated  # Allow any user to access these views
# from rest_framework.response import Response
# from .serializers import RegisterSerializer, LoginSerializer
# from pets.models import Pet  # Import the Pet model
# from django.contrib.auth.models import User  # Import User model
# from rest_framework_simplejwt.tokens import RefreshToken
# from django.contrib.auth import authenticate
# from authentication.utils import generate_hex_username
# from django.db import transaction, IntegrityError
# from django.contrib.auth import get_user_model

# User = get_user_model()

# ### ✅ Forgot Password View (Request Password Reset)
# @api_view(["POST"])
# @permission_classes([AllowAny])
# def forgot_password(request):
#     """Handles password reset requests."""
#     email = request.data.get("email")

#     try:
#         user = User.objects.get(email=email)
#     except User.DoesNotExist:
#         return Response({"error": "No account found with this email."}, status=status.HTTP_404_NOT_FOUND)

#     # ❌ Prevent sending reset link if user is not active
#     if not user.is_active:
#         return Response({"error": "This account is inactive. Please contact support."}, status=status.HTTP_400_BAD_REQUEST)

#     # ✅ Generate a password reset token & expiry time (1 hour)
#     user.password_reset_token = str(uuid.uuid4())
#     user.password_reset_expires = now() + timedelta(hours=1)
#     user.save()

#     # ✅ Send email with reset link
#     reset_url = f"http://127.0.0.1:8000/api/auth/reset-password/{user.password_reset_token}/"
#     subject = "Reset Your Password"
#     message = f"Click the link below to reset your password:\n\n{reset_url}"
    
#     send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])

#     return Response({"message": "Password reset email sent!"}, status=status.HTTP_200_OK)

# @api_view(["POST"])
# def reset_password(request, token):
#     """Handles password reset."""
#     try:
#         user = User.objects.get(password_reset_token=token)
#     except User.DoesNotExist:
#         return Response({"error": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)

#     # ✅ Check if token is expired
#     if user.password_reset_expires and user.password_reset_expires < now():
#         return Response({"error": "Password reset link has expired."}, status=status.HTTP_400_BAD_REQUEST)

#     new_password = request.data.get("password")
#     if not new_password:
#         return Response({"error": "Password is required."}, status=status.HTTP_400_BAD_REQUEST)

#     # ✅ Set new password & clear reset token
#     user.set_password(new_password)
#     user.clear_password_reset_token()
    
#     return Response({"message": "Password reset successfully!"}, status=status.HTTP_200_OK)


# @api_view(["POST"])
# @permission_classes([AllowAny])
# def register(request):
#     """Handles user registration and sends a verification email."""
#     serializer = RegisterSerializer(data=request.data)

#     if serializer.is_valid():
#         user = serializer.save()  # Serializer handles user creation & email sending
#         return Response({
#             "message": "User registered! Check your email to verify your account."
#         }, status=status.HTTP_201_CREATED)

#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# # ✅ Fixed Login View (JWT)
# @api_view(['POST'])
# @permission_classes([AllowAny])  # Allow anyone to login
# def login(request):
#     print("Received request data:", request.data)  # Debugging line
#     serializer = LoginSerializer(data=request.data)
#     if serializer.is_valid():
#         user = serializer.validated_data["user"]  # Extract user
#         refresh = RefreshToken.for_user(user)  # Generate JWT tokens
#         return Response({
#             "access": str(refresh.access_token),
#             "refresh": str(refresh),
#             "username": user.username,
#         }, status=status.HTTP_200_OK)
#     print("Login errors:", serializer.errors)  # Debugging line
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# # ✅ New View: Fetch user details
# @api_view(['GET'])
# @permission_classes([IsAuthenticated])  # Only allow authenticated users
# def get_user_details(request):
#     user = request.user
#     return Response({
#         "id": user.id,
#         "username": user.username,
#         "email": user.email,
#     }, status=status.HTTP_200_OK)



# @api_view(["DELETE"])
# @permission_classes([IsAuthenticated])
# def delete_user(request):
#     user = request.user
#     user.delete()
#     return Response({"message": "User deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

# @api_view(["POST"])
# @permission_classes([IsAuthenticated])
# def logout(request):
#     try:
#         refresh_token = request.data["refresh"]
#         token = RefreshToken(refresh_token)
#         token.blacklist()  # Blacklist the token
#         return Response({"message": "Logout successful"}, status=status.HTTP_205_RESET_CONTENT)
#     except Exception as e:
#         return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['POST'])
# @permission_classes([AllowAny])
# def register(request):
#     serializer = RegisterSerializer(data=request.data)

#     if serializer.is_valid():
#         email = serializer.validated_data["email"]
#         password = serializer.validated_data["password"]

#         try:
#             with transaction.atomic():  # ✅ Prevents race conditions!
#                 user, created = User.objects.get_or_create(
#                     email=email,
#                     defaults={"username": generate_hex_username()}
#                 )

#                 if not created:
#                     return Response({"error": "Email is already registered!"}, status=status.HTTP_400_BAD_REQUEST)

#                 user.set_password(password)  # ✅ Hash the password manually
#                 user.save()

#             return Response({
#                 'message': 'User created successfully',
#                 'username': user.username
#             }, status=status.HTTP_201_CREATED)

#         except IntegrityError:
#             return Response({"error": "Email is already registered!"}, status=status.HTTP_400_BAD_REQUEST)

#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# @api_view(['POST'])
# @permission_classes([AllowAny])
# def register(request):
#     serializer = RegisterSerializer(data=request.data)

#     if serializer.is_valid():
#         email = serializer.validated_data["email"]

#         # ✅ Check if user already exists before creating
#         if User.objects.filter(email=email).exists():
#             return Response({"error": "Email is already registered!"}, status=status.HTTP_400_BAD_REQUEST)

#         # ✅ Generate a unique username
#         username = generate_hex_username()

#         # ✅ Create the user manually
#         user = User.objects.create_user(
#             username=username,
#             email=email,
#             password=serializer.validated_data["password"]
#         )

#         return Response({
#             'message': 'User created successfully',
#             'username': user.username
#         }, status=status.HTTP_201_CREATED)

#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['POST'])
# @permission_classes([AllowAny])
# def register(request):
#     serializer = RegisterSerializer(data=request.data)

#     if serializer.is_valid():
#         # ✅ Generate a unique username
#         username = generate_hex_username()

#         # ✅ Create the user manually in `views.py`
#         user = User.objects.create_user(
#             username=username,
#             email=serializer.validated_data["email"],
#             password=serializer.validated_data["password"]  # ✅ Hashes password automatically
#         )

#         return Response({
#             'message': 'User created successfully',
#             'username': user.username
#         }, status=status.HTTP_201_CREATED)

#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['POST'])
# @permission_classes([AllowAny])
# def register(request):
#     serializer = RegisterSerializer(data=request.data)

#     if serializer.is_valid():
#         user = serializer.save()  # ✅ Calls `create()` in serializer (No duplicates!)

#         return Response({
#             'message': 'User created successfully',
#             'username': user.username
#         }, status=status.HTTP_201_CREATED)

#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['POST'])
# @permission_classes([AllowAny])
# def register(request):
#     serializer = RegisterSerializer(data=request.data)

#     if serializer.is_valid():
#         user = serializer.save()  # ✅ Create user, but don't log them in

#         return Response({
#             'message': 'User created successfully',
#             'username': user.username
#         }, status=status.HTTP_201_CREATED)  # ✅ No JWT tokens returned

#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# @api_view(['POST'])
# @permission_classes([AllowAny])
# def register(request):
#     serializer = RegisterSerializer(data=request.data)

#     if serializer.is_valid():
#         user = serializer.save()  # ✅ No need to manually create the user (handled in serializer)

#         # ✅ (Optional) Automatically log in the user
#         refresh = RefreshToken.for_user(user)
#         access_token = str(refresh.access_token)

#         return Response({
#             'message': 'User created successfully',
#             'username': user.username,
#             'access_token': access_token,
#             'refresh_token': str(refresh)
#         }, status=status.HTTP_201_CREATED)

#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# Register View
# @api_view(['POST'])
# @permission_classes([AllowAny]) # Anyone anyone to register
# def register(request):
#     serializer = RegisterSerializer(data=request.data)
#     if serializer.is_valid():
#         user = serializer.save()
#         return Response({'message': 'User created successfully', 'username': user.username}, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# Login View (JWT token-based)
# @api_view(['POST'])
# @permission_classes([AllowAny])  # Allow anyone to login
# def login(request):
#     if request.method == 'POST':
#         serializer = LoginSerializer(data=request.data)
#         if serializer.is_valid():
#             return Response(serializer.validated_data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    
# @api_view(["DELETE"])
# @permission_classes([IsAuthenticated])
# def delete_user(request):
#     user = request.user
#     user.is_active = False  # Soft delete
#     user.save()
#     return Response({"message": "User deactivated successfully"}, status=status.HTTP_204_NO_CONTENT)

