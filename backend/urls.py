"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings #
from django.conf.urls.static import static #

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('authentication.urls')),  # Include authentication routes
    path('api/pets/', include('pets.urls')), # Include the pets app's URLs
    path('api/user-profile/', include('user_profile.urls')),  # Link the user_profile app's URLs here
    path('api/shelters/', include('shelters.urls')), # Include the shelters app's URLs
    path('api/articles/', include('articles.urls')),  # API routes for articles
    path('api/', include('articles.urls')),  # Include the articles app's URLs under 'api/'
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



# 9. Protecting Routes with Authentication
# To ensure that certain views or endpoints require authentication, you can use the IsAuthenticated permission class:
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.views import APIView

# class ProtectedView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         return Response({"message": "This is a protected view!"})