from rest_framework import serializers
from accounts.models import User
from datetime import date
from .models import Class, Student, Attendance, WeeklySchedule, Lesson
from drf_writable_nested.serializers import WritableNestedModelSerializer

class StudentSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(read_only=True)
    class Meta:
        model = Student
        fields = ["id", "first_name", "last_name", "number", "student_id", "serial_code", "class_room", "full_name"]
    
    def validate_number(self, value):
        if len(value) != 11:
            message = 'phone number length should be 11.'
            raise serializers.ValidationError(message)
        try:
            int(value)
        except ValueError:
            message = 'it should be a valid number'
            raise serializers.ValidationError(message)
        return value
    
    def validate_student_id(self, value):
        if len(value) != 10:
            message = 'id length should be 10.'
            raise serializers.ValidationError(message)
        try:
            int(value)
        except ValueError:
            message = 'it should be a valid number'
            raise serializers.ValidationError(message)
        return value
    
    def validate_serial_code(self, value):
        if len(value) != 6:
            message = 'serial code length should be 10.'
            raise serializers.ValidationError(message)
        try:
            int(value)
        except ValueError:
            message = 'it should be a valid number'
            raise serializers.ValidationError(message)
        return value

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
    
    def create(self, validated_data):
        obj, _ = Lesson.objects.get_or_create(**validated_data)
        return obj

class WeeklyScheduleSerializer(WritableNestedModelSerializer):
    satureday = LessonSerializer(many=True)
    sunday = LessonSerializer(many=True)
    monday = LessonSerializer(many=True)
    tuesday = LessonSerializer(many=True)
    wednesday = LessonSerializer(many=True)

    class Meta:
        model = WeeklySchedule
        fields = '__all__'

class ClassStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ["id", "full_name", "number"]

class ClassListSerializer(serializers.ModelSerializer):
    students_count = serializers.IntegerField()
    class Meta:
        model = Class
        fields = ["class_id", "students_count"]

class ClassSerializer(WritableNestedModelSerializer):
    students = ClassStudentSerializer(many=True, read_only=True)
    students_count = serializers.IntegerField(read_only=True)
    weekly_schedule = WeeklyScheduleSerializer(required=False)
    class Meta:
        model = Class
        fields = ["class_id", "students", "students_count", "weekly_schedule"]

class AttendanceSerializer(serializers.ModelSerializer):
    presents = StudentSerializer(many=True)
    absents = StudentSerializer(many=True)
    class_room = serializers.CharField(source='class_room.class_id', read_only=True)
    class Meta:
        model = Attendance
        fields = ["id", "class_room", "absents", "presents", "date"]

class AttendanceCreateSerializer(serializers.ModelSerializer):
    class_room = serializers.PrimaryKeyRelatedField(read_only=True)
    date = serializers.DateField(default=date.today)
    class Meta:
        model = Attendance
        fields = ['class_room', 'absents', 'presents', 'date']


class AttendanceListSerializer(serializers.ModelSerializer):
    class_room = serializers.CharField(source='class_room.class_id', read_only=True)
    absents_count = serializers.IntegerField(source='absents.count', read_only=True)
    detail = serializers.HyperlinkedIdentityField(view_name="attendance-detail", read_only=True)
    class Meta:
        model = Attendance
        fields = ["id", "class_room", "date", "absents_count", "detail"]