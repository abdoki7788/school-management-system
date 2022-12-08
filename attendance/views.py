from django.contrib.auth import get_user_model
from rest_framework import viewsets
from .serializers import ClassSerializer
from .models import Class

User = get_user_model()

class ClassViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """
    serializer_class = ClassSerializer
    queryset = Class.objects.all()