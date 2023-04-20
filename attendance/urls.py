from django.urls import path

from rest_framework.routers import DefaultRouter
from .views import ClassViewSet, StudentViewSet, DashboardHome


# added all viewsets to router
router = DefaultRouter()
router.register(r'classes', ClassViewSet, basename='class')
router.register(r'students', StudentViewSet, basename='student')

urlpatterns = [
    path('dashboard/', DashboardHome.as_view(), name='dashboard-home')
]

urlpatterns += router.urls