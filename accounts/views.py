from django.shortcuts import render
from django.contrib.auth import get_user_model

from rest_framework.response import Response

from djoser.views import TokenCreateView, UserViewSet as JUserViewSet
from djoser.conf import settings
from djoser import utils

# Create your views here.

User = get_user_model()

class CustomTokenCreateView(TokenCreateView):
    authentication_classes = []

class UserViewSet(JUserViewSet):
    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = settings.PERMISSIONS.user_create
        elif self.action == "list":
            self.permission_classes = settings.PERMISSIONS.user_list
        elif self.action == "destroy" or (
            self.action == "me" and self.request and self.request.method == "DELETE"
        ):
            self.permission_classes = settings.PERMISSIONS.user_delete
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == "create":
            if settings.USER_CREATE_PASSWORD_RETYPE:
                return settings.SERIALIZERS.user_create_password_retype
            return settings.SERIALIZERS.user_create
        elif self.action == "destroy" or (
            self.action == "me" and self.request and self.request.method == "DELETE"
        ):
            return settings.SERIALIZERS.user_delete
        elif self.action == "me":
            return settings.SERIALIZERS.current_user

        return self.serializer_class
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance == request.user:
            utils.logout_user(self.request)
        self.perform_destroy(instance)
        return Response(status=204)

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def activation(self):
        pass
    def resend_activation(self):
        pass
    def set_password(self):
        pass
    def reset_password(self):
        pass
    def set_username(self):
        pass
    def reset_password_confirm(self):
        pass
    def reset_username(self):
        pass
    def reset_username_confirm(self):
        pass