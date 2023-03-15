import datetime
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.db.utils import IntegrityError
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django_filters import rest_framework as filters
from .serializers import ClassSerializer, ClassListSerializer, StudentSerializer, AttendanceListSerializer, AttendanceSerializer, AttendanceCreateSerializer
from .permissions import IsHeadmasterOrReadonly, IsSchoolStaffOrReadOnly
from .models import Class, Student, Attendance

User = get_user_model()


# Students Filterset
class StudentFilterSet(filters.FilterSet):
    class_id = filters.CharFilter(field_name='class_room__class_id')



class StudentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsSchoolStaffOrReadOnly]
    serializer_class = StudentSerializer
    queryset = Student.objects.all()
    filterset_class = StudentFilterSet
    @action(detail=True, methods=["GET"])
    def absents(self, request, pk):
        student = self.get_object()
        return Response({
            "absents_count": student.absent.count(),
            "absent": [i.date for i in student.absent.all()]

        })


class ClassViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsSchoolStaffOrReadOnly]
    serializer_class = ClassSerializer
    queryset = Class.objects.all().order_by('-class_id')
    lookup_field = 'class_id'

    def get_serializer_class(self):
        if self.action == 'list':
            return ClassListSerializer
        return super().get_serializer_class()
    
    @action(detail=True, methods=['GET', 'POST'], serializer_class=AttendanceCreateSerializer)
    def attendances(self, request, class_id):
        obj = self.get_object()
        if request.method == 'GET':
            return Response(
                AttendanceListSerializer(obj.attendances, many=True, context = {
                    'request': request,
                }).data
            )
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


    @action(detail=True, methods=['GET'], url_path=r'attendances/(?P<attendance_date>(\d{4}-\d{2}-\d{2}))')
    def attendance(self, request, class_id, attendance_date):
        obj = self.get_object()
        serialized_data = AttendanceSerializer(get_object_or_404(obj.attendances, date=attendance_date))
        return Response(serialized_data.data)
    
    @action(detail=True, methods=['GET', 'POST'])
    def today_attendance(self, request, class_id):
        obj = self.get_object()
        if request.method == 'GET':
            try:
                today = obj.attendances.get(date=datetime.date.today())
                return Response(
                    AttendanceSerializer(today).data
                )
            except Attendance.DoesNotExist:
                raise NotFound(detail='there is no attendance today for this class')
        elif request.method == 'POST':
            try:
                obj.attendances.get(date=datetime.date.today())
                return Response(
                    {'detail': 'attendance for today is already exist'}, 
                    status=400
                )
            except Attendance.DoesNotExist:
                serialized_attendance = AttendanceCreateSerializer(data=request.data)
                if serialized_attendance.is_valid():
                    try:
                        serialized_attendance.save(class_room=obj, date=datetime.date.today())
                        return Response(serialized_attendance.data, status=201)
                    except:
                        return Response(
                            {'detail': "attendance object cant be created"}, 
                            status=400
                        )
                else:
                    return Response(serialized_attendance.errors)

class AttendanceViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsSchoolStaffOrReadOnly]
    queryset = Attendance.objects.all()
    filterset_fields = ['date']

    def get_serializer_class(self):
        if self.action == 'list':
            return AttendanceListSerializer
        else:
            return AttendanceSerializer