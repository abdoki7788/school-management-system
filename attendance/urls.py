from rest_framework.routers import DefaultRouter
from .views import ClassViewSet, StudentViewSet


# added all viewsets to router
router = DefaultRouter()
router.register(r'classes', ClassViewSet, basename='class')
router.register(r'students', StudentViewSet, basename='student')


urlpatterns = router.urls