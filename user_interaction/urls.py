from django.urls import path, include
from rest_framework import routers
from .views import UserInteractionAPIViewSet

default_router = routers.DefaultRouter(trailing_slash=False)

default_router.register('interactions', UserInteractionAPIViewSet, basename='interaction')

urlpatterns = [
    path('', include(default_router.urls))
]
