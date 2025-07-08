from rest_framework import serializers
from .models import WashStation, Employee, Service, Car

class WashStationSerializer(serializers.ModelSerializer):
    class Meta:
        model = WashStation
        fields = '__all__'
        read_only_fields = ['user_id']  # пользователь сам не указывает

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'

class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = '__all__'
