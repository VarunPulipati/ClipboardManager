from django.urls import path, include
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),  # DRF browsable API auth
    path('api/', include('api.urls')),  # Include your app's URLs here
]
