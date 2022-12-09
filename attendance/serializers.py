from rest_framework import serializers
from .models import Class, Student

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ["id", "first_name", "last_name", "number"]

class ClassSerializer(serializers.ModelSerializer):
    students = StudentSerializer(many=True)
    class Meta:
        model = Class
        fields = ["id", "class_id", "students"]