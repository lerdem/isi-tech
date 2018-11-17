from django.contrib.auth import get_user_model
from rest_framework import permissions, viewsets, mixins

from .serializer import (
    CreateThreadSerializer,
    ThreadSerializer,
    CreateMessageSerializer
)

User = get_user_model()

class IsUserAdminType(permissions.BasePermission):
    """
    Allows access only for user type admin.
    """

    def has_permission(self, request, view):
        return request.user.type == User.ADMIN


class ThreadViewSet(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):

    serializer_class_map = {
        'create': CreateThreadSerializer,
        'list': ThreadSerializer,
    }

    @property
    def permission_classes(self):
        if self.action == 'create':
            return (IsUserAdminType, )
        return (permissions.IsAuthenticated, )

    def get_queryset(self):
        from .models import Thread
        return Thread.objects.filter(participants=self.request.user)

    def get_serializer_class(self):
        return self.serializer_class_map[self.action]


class MessageViewSet(mixins.CreateModelMixin,
                    viewsets.GenericViewSet):

    serializer_class_map = {
        'create': CreateMessageSerializer,
    }

    def get_serializer_class(self):
        return self.serializer_class_map[self.action]
