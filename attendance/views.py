from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .serializers import ClassSerializer, StudentSerializer
from .permissions import IsHeadmasterOrReadonly, IsSchoolStaffOrReadOnly
from .models import Class, Student

User = get_user_model()

class StudentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsSchoolStaffOrReadOnly]
    serializer_class = StudentSerializer
    queryset = Student.objects.all()

class ClassViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsHeadmasterOrReadonly]
    serializer_class = ClassSerializer
    queryset = Class.objects.all()