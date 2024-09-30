from rest_framework import viewsets
from .models import Shortcut
from .serializers import ShortcutSerializer

class ShortcutViewSet(viewsets.ModelViewSet):
    queryset = Shortcut.objects.all()
    serializer_class = ShortcutSerializer
