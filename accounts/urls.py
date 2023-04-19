from django.urls import path
from djoser.views import TokenDestroyView
from .views import CustomTokenCreateView, UserViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register("users", UserViewSet)

urlpatterns = [
    path("token/login/", CustomTokenCreateView.as_view(), name="login"),
    path("token/logout/", TokenDestroyView.as_view(), name="logout"),
]

urlpatterns = router.urls