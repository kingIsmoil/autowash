from rest_framework.decorators import action
from django.utils.timezone import now
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Sum, Count
from rest_framework.response import Response
from .filters import CarFilter
from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend
from .models import WashStation, Employee, Service, Car
from .serializers import WashStationSerializer, EmployeeSerializer, ServiceSerializer, CarSerializer
from django.core.cache import cache


class WashStationViewSet(viewsets.ModelViewSet):
    serializer_class = WashStationSerializer
    permission_classes = [permissions.IsAuthenticated]
    swagger_tags = ['Wash Station']

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return WashStation.objects.filter(user_id=user)
        return WashStation.objects.none()


    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user)



class EmployeeViewSet(viewsets.ModelViewSet):
    serializer_class = EmployeeSerializer
    permission_classes = [permissions.IsAuthenticated]
    swagger_tags = ['Employee']
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name']

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Employee.objects.filter(wash_id__user_id=user)
        return Employee.objects.none()



class ServiceViewSet(viewsets.ModelViewSet):
    serializer_class = ServiceSerializer
    permission_classes = [permissions.IsAuthenticated]
    swagger_tags = ['Service']

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Service.objects.filter(wash_id__user_id=user)
        return Service.objects.none()




class CarViewSet(viewsets.ModelViewSet):
    serializer_class = CarSerializer
    permission_classes = [permissions.IsAuthenticated]
    swagger_tags = ['Car']
    filter_backends = [DjangoFilterBackend]
    filterset_class = CarFilter

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Car.objects.filter(wash_id__user_id=user)
        return Car.objects.none()

    @action(detail=False, methods=['get'], url_path='totals')
    def totals(self, request):
        """
        Показывает:
        - total за всё время
        - total за сегодня
        - total по заданному фильтру (entry_time__gte / lte)
        """
        user = request.user
        cache_key = f"totals_user_{user.id}"
        cached = cache.get(cache_key)
        if cached:
            return Response(cached)
        
        base_queryset = self.get_queryset()
        filtered_queryset = CarFilter(request.GET, queryset=base_queryset).qs
        total_all = base_queryset.aggregate(
            total_cars=Count('id'),
            total_price=Sum('service_id__price')
        )
        today = now().date()
        today_queryset = base_queryset.filter(entry_time__date=today)
        total_today = today_queryset.aggregate(
            total_cars=Count('id'),
            total_price=Sum('service_id__price')
        )
        total_filtered = filtered_queryset.aggregate(
            total_cars=Count('id'),
            total_price=Sum('service_id__price')
        )
        result = {
            'total_all': {
                'total_cars': total_all['total_cars'] or 0,
                'total_price': total_all['total_price'] or 0
            },
            'total_today': {
                'total_cars': total_today['total_cars'] or 0,
                'total_price': total_today['total_price'] or 0
            },
            'total_filtered': {
                'total_cars': total_filtered['total_cars'] or 0,
                'total_price': total_filtered['total_price'] or 0
            }
        }
        cache.set(cache_key, result, timeout=60)
        return Response(result)



