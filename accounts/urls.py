from django.urls import path
from djoser.views import TokenDestroyView
from .views import CustomTokenCreateView

urlpatterns = [
    path("token/login/", CustomTokenCreateView.as_view(), name="login"),
    path("token/logout/", TokenDestroyView.as_view(), name="logout"),
]
