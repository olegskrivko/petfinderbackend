from django.urls import path
from . import views
from dj_rest_auth.views import LoginView, LogoutView
from rest_framework_simplejwt.views import TokenRefreshView
from .views import forgot_password, reset_password, activate_user, login, logout

urlpatterns = [
    path('register/', views.register, name='register'),
    # path('login/', views.login, name='login'), # Login (Get JWT)
    path('login/', login, name='login'),
    #path("login/", LoginView.as_view(), name="login"),  # ✅ Built-in login (handles JWT)
    #path('logout/', LogoutView.as_view(), name='logout'),  # Logout
    #path('logout/', LogoutView.as_view(), name='logout'),  # Logout
    path('logout/', logout, name='logout'),
    path("forgot-password/", forgot_password, name="forgot_password"),
    path("reset-password/<str:token>/", reset_password, name="reset_password"),  # ✅ This MUST match the frontend URL!
    path("activate/<str:token>/", activate_user, name="activate"),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Refresh JWT
    path('user/', views.get_user_details, name='user-details'),  # ✅ New endpoint
    path("user/delete/", views.delete_user, name="delete-user"),
]
