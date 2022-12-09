from django.contrib.auth import get_user_model
from rest_framework import viewsets
from .serializers import ClassSerializer
from .permissions import IsHeadmasterOrReadonly
from .models import Class

User = get_user_model()

class ClassViewSet(viewsets.ModelViewSet):
    permission_classes = [IsHeadmasterOrReadonly]
    serializer_class = ClassSerializer
    queryset = Class.objects.all()