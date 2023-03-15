from rest_framework import serializers
from accounts.models import User
from datetime import date
from .models import Class, Student, Attendance

class StudentSerializer(serializers.ModelSerializer):
    class_room = serializers.CharField(source='class_room.class_id', read_only=True)
    full_name = serializers.CharField(read_only=True)
    class Meta:
        model = Student
        fields = ["id", "first_name", "last_name", "number", "class_room", "full_name"]
    
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

class ClassStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ["id", "full_name", "number"]

class ClassListSerializer(serializers.ModelSerializer):
    students_count = serializers.IntegerField()
    class Meta:
        model = Class
        fields = ["class_id", "students_count"]

class ClassSerializer(serializers.ModelSerializer):
    students = ClassStudentSerializer(many=True, read_only=True)
    students_count = serializers.IntegerField(read_only=True)
    class Meta:
        model = Class
        fields = ["class_id", "students", "students_count"]

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