from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    ThreadViewSet,
    MessageViewSet
)


router = DefaultRouter()
router.register(r'v1/thread', ThreadViewSet, base_name='thread')
router.register(r'v1/message', MessageViewSet, base_name='message')


urlpatterns = [
    path('', include(router.urls)),
]