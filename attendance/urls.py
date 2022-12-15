from rest_framework.routers import DefaultRouter
from .views import ClassViewSet, StudentViewSet, AttendanceViewSet

router = DefaultRouter()
router.register(r'classes', ClassViewSet, basename='class')
router.register(r'students', StudentViewSet, basename='student')
router.register(r'attendances', AttendanceViewSet, basename='attendance')


urlpatterns = router.urls