from rest_framework import serializers
from drf_writable_nested.serializers import WritableNestedModelSerializer

from .models import Class, Student, Attendance, WeeklySchedule, Lesson
from accounts.serializers import CustomChoiceField

## serializer for students view . for creating, updating and getting
class StudentSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(read_only=True)
    discipline = CustomChoiceField(Student.DISCIPLINE_CHOICES)
    class Meta:
        model = Student
        fields = ["id", "first_name", "last_name", "number", "student_id", "serial_code", "class_room", "full_name", "image", "discipline"]
        extra_kwargs = {"class_room": {"required": False}}


## serializer for lessons
class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        validators = []
        fields = '__all__'
        ordering = '-priority'
    
    ## some extra functionalities on lesson save for get if lesson was created
    def save(self, **kwargs):
        validated_data = {**self.validated_data, **kwargs}
        print(validated_data)
        qs = Lesson.objects.filter(lesson_name=validated_data['lesson_name'], teacher=validated_data['teacher'])
        if qs.exists():
            self.instance = qs.first()
        return super().save(**kwargs)

## weekly schedule serializer with Writable Nested Serializer library
class WeeklyScheduleSerializer(WritableNestedModelSerializer):
    satureday = LessonSerializer(many=True)
    sunday = LessonSerializer(many=True)
    monday = LessonSerializer(many=True)
    tuesday = LessonSerializer(many=True)
    wednesday = LessonSerializer(many=True)

    class Meta:
        model = WeeklySchedule
        exclude = ['id']


## student serializer for showing in class views
class ClassStudentSerializer(serializers.ModelSerializer):
    discipline = CustomChoiceField(Student.DISCIPLINE_CHOICES)
    class Meta:
        model = Student
        fields = ["id", "full_name", "number", "student_id", "serial_code", "image", "discipline"]

## class serializer for showing list
class ClassListSerializer(serializers.ModelSerializer):
    students_count = serializers.IntegerField()
    class Meta:
        model = Class
        fields = ["class_id", "students_count"]

## class serializer for showing generally and creating & updating
class ClassSerializer(WritableNestedModelSerializer):
    students = ClassStudentSerializer(many=True, read_only=True)
    students_count = serializers.IntegerField(read_only=True)
    weekly_schedule = WeeklyScheduleSerializer(required=False)
    class Meta:
        model = Class
        fields = ["class_id", "students", "students_count", "weekly_schedule"]


## dashboard class serializer
class DashboardClassSerializer(serializers.ModelSerializer):
    students = ClassStudentSerializer(many=True, read_only=True)
    class Meta:
        model = Class
        fields = ["class_id", "students"]


###     Attendance System Functionalities Commented Because of Lack of time to complete


# class AttendanceSerializer(serializers.ModelSerializer):
#     presents = StudentSerializer(many=True)
#     absents = StudentSerializer(many=True)
#     class_room = serializers.CharField(source='class_room.class_id', read_only=True)
#     class Meta:
#         model = Attendance
#         fields = ["id", "class_room", "absents", "presents", "date"]

# class AttendanceCreateSerializer(serializers.ModelSerializer):
#     class_room = serializers.PrimaryKeyRelatedField(read_only=True)
#     date = serializers.DateField(default=date.today)
#     class Meta:
#         model = Attendance
#         fields = ['class_room', 'absents', 'presents', 'date']


# class AttendanceListSerializer(serializers.ModelSerializer):
#     class_room = serializers.CharField(source='class_room.class_id', read_only=True)
#     absents_count = serializers.IntegerField(source='absents.count', read_only=True)
#     detail = serializers.HyperlinkedIdentityField(view_name="attendance-detail", read_only=True)
#     class Meta:
#         model = Attendance
#         fields = ["id", "class_room", "date", "absents_count", "detail"]