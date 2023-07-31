from django.shortcuts import render
from django.contrib.auth import get_user_model

from rest_framework.response import Response
from rest_framework.decorators import action

from djoser.views import TokenCreateView, UserViewSet as JUserViewSet
from djoser.conf import settings
from djoser import utils

from .serializers import CustomUserSerializer, UserCreateSerializerNoType

# Create your views here.

User = get_user_model()

class CustomTokenCreateView(TokenCreateView):
    authentication_classes = []

class UserViewSet(JUserViewSet):

    def user_type_view(self, request, type, *args, **kwargs):
        if request.method.lower() == "get":
            q = User.objects.filter(type=type)
            serializer = CustomUserSerializer(q, many=True)
            return Response(serializer.data, status=200)
        else:
            serializer = UserCreateSerializerNoType(data=request.data)
            if serializer.is_valid():
                serializer.validated_data["type"] = type
                self.perform_create(serializer)
                return Response(serializer.data, status=201)
            else:
                return Response(serializer.errors, status=400)

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        print(self.action)
        if settings.HIDE_USERS and self.action == "list" and not user.is_staff:
            queryset = queryset.filter(pk=user.pk)
        if self.action == 'list':
            queryset = queryset.exclude(pk=user.pk)
        return queryset

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
    
    @action(["get", "post"], False)
    def teachers(self, request, *args, **kwargs):
        return self.user_type_view(request, "T", *args, **kwargs)
    
    @action(["get", "post"], False)
    def staffs(self, request, *args, **kwargs):
        return self.user_type_view(request, "S", *args, **kwargs)
    
    @action(["get", "post"], False)
    def headmasters(self, request, *args, **kwargs):
        return self.user_type_view(request, "H", *args, **kwargs)
        

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