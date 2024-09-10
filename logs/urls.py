from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LogViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
router = DefaultRouter()
router.register(r'logs', LogViewSet, basename='log')

urlpatterns = [
    path('', include(router.urls)),
]
