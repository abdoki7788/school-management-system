from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.db.utils import IntegrityError
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from .serializers import ClassSerializer, StudentSerializer, AttendanceListSerializer, AttendanceSerializer, AttendanceCreateSerializer
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

    @action(detail=True, methods=['GET', 'POST'], serializer_class=AttendanceCreateSerializer)
    def attendances(self, request, class_id):
        obj = self.get_object()
        print(request.method)
        if request.method == 'GET':
            return Response(AttendanceListSerializer(obj.attendances, many=True).data)
        elif request.method == 'POST':
            serialized_data = AttendanceCreateSerializer(data=request.data)
            if serialized_data.is_valid():
                try:
                    serialized_data.save(class_room=obj)
                    return Response(serialized_data.data, status=201)
                except IntegrityError:
                    return Response({'error': "attendance object cant be created"}, status=400)
            else:
                return Response(serialized_data.errors)


    @action(detail=True, methods=['GET'], url_path=r'attendances/(?P<attendance_id>[a-z0-9]+)')
    def attendance(self, request, class_id, attendance_id):
        obj = self.get_object()
        serialized_data = AttendanceSerializer(get_object_or_404(obj.attendances, id=attendance_id))
        return Response(serialized_data.data)

class AttendanceViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsSchoolStaffOrReadOnly]
    queryset = Attendance.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return AttendanceListSerializer
        else:
            return AttendanceSerializer