# api/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ShortcutViewSet

router = DefaultRouter()
router.register(r'shortcuts', ShortcutViewSet)

urlpatterns = [
    path('', include(router.urls)),

]
