# django
from django.contrib.auth import get_user_model

# rest framework
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from django_filters import rest_framework as filters

# local imports
from .serializers import ClassSerializer, ClassStudentSerializer, ClassListSerializer, StudentSerializer, DashboardClassSerializer
from .permissions import IsSchoolStaffOrReadOnly, IsHeadmaster
from .models import Class, Student, Attendance

import datetime


# Get Current User Model
User = get_user_model()


# Students Filterset
class StudentFilterSet(filters.FilterSet):
    class_id = filters.CharFilter(field_name='class_room__class_id')



# Set of Student endpoints .
#  functionality of creating, updating, getting and listing students

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


# Set of Class Views for creating, updating, deleting and getting classes
# wirh extra functionalities like get and create students for the class

class ClassViewSet(viewsets.ModelViewSet):
    # this view can be edited(POST, PUT, PATCH) just By adminstrators(headmaster of school and school staffs)
    permission_classes = [IsAuthenticated, IsSchoolStaffOrReadOnly]

    serializer_class = ClassSerializer
    # classes ordered by their Expected age
    queryset = Class.objects.all().order_by('-class_id')

    lookup_field = 'class_id'

    def get_serializer_class(self):
        if self.action == 'list':
            return ClassListSerializer
        return super().get_serializer_class()
    
    # "/students" section of each class
    @action(detail=True, methods=['GET', 'POST'])
    def students(self, request, class_id):
        obj = self.get_object()
        # the get method: for getting students of the class
        if request.method.lower() == 'get':
            return Response(ClassStudentSerializer(obj.students, many=True, context={'request': request}).data)
        
        # the post method: for creating students of class
        if request.method.lower() == 'post':
            serialized_data = StudentSerializer(data=request.data, context={'request': request})

            ## if the data was valid , create student. else return errors
            if serialized_data.is_valid():
                serialized_data.save(class_room=obj)
                return Response(serialized_data.data, status=201)
            else:
                return Response(serialized_data.errors, status=400)


## view for dashboard home ( just get method )
class DashboardHome(APIView):
    permission_classes = [IsHeadmaster]

    def get(self, request, *args, **kwargs):
        staff_count = User.objects.count()
        students_count = Student.objects.count()
        classes_count = Class.objects.count()

        # get all classes with their students
        classes = DashboardClassSerializer(Class.objects.all(), many=True, context={'request': request})

        return Response({
            'staff_count': staff_count, 
            'students_count': students_count, 
            'classes_count': classes_count,
            'classes': classes.data
        })




    ###       Attendance System Functionalities Commented Because of Lack of time to complete

    # @action(detail=True, methods=['GET', 'POST'], serializer_class=AttendanceCreateSerializer)
    # def attendances(self, request, class_id):
    #     obj = self.get_object()
    #     if request.method == 'GET':
    #         return Response(
    #             AttendanceListSerializer(obj.attendances, many=True, context = {
    #                 'request': request,
    #             }).data
    #         )
    #     elif request.method == 'POST':
    #         serialized_data = AttendanceCreateSerializer(data=request.data)
    #         if serialized_data.is_valid():
    #             try:
    #                 serialized_data.save(class_room=obj)
    #                 return Response(serialized_data.data, status=201)
    #             except IntegrityError:
    #                 return Response({'error': "attendance object cant be created"}, status=400)
    #         else:
    #             return Response(serialized_data.errors, 401)


    # @action(detail=True, methods=['GET'], url_path=r'attendances/(?P<attendance_date>(\d{4}-\d{2}-\d{2}))')
    # def attendance(self, request, class_id, attendance_date):
    #     obj = self.get_object()
    #     serialized_data = AttendanceSerializer(get_object_or_404(obj.attendances, date=attendance_date))
    #     return Response(serialized_data.data)
    
    # @action(detail=True, methods=['GET', 'POST'])
    # def today_attendance(self, request, class_id):
    #     obj = self.get_object()
    #     if request.method == 'GET':
    #         try:
    #             today = obj.attendances.get(date=datetime.date.today())
    #             return Response(
    #                 AttendanceSerializer(today).data
    #             )
    #         except Attendance.DoesNotExist:
    #             raise NotFound(detail='there is no attendance today for this class')
    #     elif request.method == 'POST':
    #         try:
    #             obj.attendances.get(date=datetime.date.today())
    #             return Response(
    #                 {'detail': 'attendance for today is already exist'}, 
    #                 status=400
    #             )
    #         except Attendance.DoesNotExist:
    #             serialized_attendance = AttendanceCreateSerializer(data=request.data)
    #             if serialized_attendance.is_valid():
    #                 try:
    #                     serialized_attendance.save(class_room=obj, date=datetime.date.today())
    #                     return Response(serialized_attendance.data, status=201)
    #                 except:
    #                     return Response(
    #                         {'detail': "attendance object cant be created"}, 
    #                         status=400
    #                     )
    #             else:
    #                 return Response(serialized_attendance.errors)

###     Attendance System Functionalities Commented Because of Lack of time to complete

# class AttendanceViewSet(viewsets.ModelViewSet):
#     permission_classes = [IsAuthenticated, IsSchoolStaffOrReadOnly]
#     queryset = Attendance.objects.all()
#     filterset_fields = ['date']

#     def get_serializer_class(self):
#         if self.action == 'list':
#             return AttendanceListSerializer
#         else:
#             return AttendanceSerializer