from rest_framework import serializers
from .models import Class, Student

class StudentSerializer(serializers.ModelSerializer):
    class_room = serializers.CharField(source='class_room.class_id', read_only=True)
    class Meta:
        model = Student
        fields = ["id", "first_name", "last_name", "number", "class_room"]



class ClassStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ["id", "first_name", "last_name", "number"]

class ClassSerializer(serializers.ModelSerializer):
    students = ClassStudentSerializer(many=True, read_only=True)
    class Meta:
        model = Class
        fields = ["id", "class_id", "students"]