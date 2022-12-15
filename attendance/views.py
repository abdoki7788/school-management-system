from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from .serializers import ClassSerializer, StudentSerializer, AttendanceListSerializer, AttendanceSerializer
from .permissions import IsHeadmasterOrReadonly, IsSchoolStaffOrReadOnly
from .models import Class, Student, Attendance

User = get_user_model()

class StudentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsSchoolStaffOrReadOnly]
    serializer_class = StudentSerializer
    queryset = Student.objects.all()
    @action(detail=True, methods=["GET"])
    def absents(self, request, pk):
        student = self.get_object()
        return Response({
            "absents_count": student.absent.count(),
            "absent": [i.date for i in student.absent.all()]

        })


class ClassViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsHeadmasterOrReadonly]
    serializer_class = ClassSerializer
    queryset = Class.objects.all()
    lookup_field = 'class_id'

    @action(detail=True, methods=['GET'])
    def attendances(self, request, class_id):
        obj = self.get_object()
        return Response(AttendanceSerializer(obj.attendances, many=True).data)

class AttendanceViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsSchoolStaffOrReadOnly]
    queryset = Attendance.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return AttendanceListSerializer
        else:
            return AttendanceSerializer