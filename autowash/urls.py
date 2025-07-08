from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WashStationViewSet, EmployeeViewSet, ServiceViewSet, CarViewSet

router = DefaultRouter()
router.register('washstations', WashStationViewSet, basename='washstation')
router.register('employees', EmployeeViewSet, basename='employee')
router.register('services', ServiceViewSet, basename='service')
router.register('cars', CarViewSet, basename='car')

urlpatterns = [
    path('', include(router.urls)),
]
