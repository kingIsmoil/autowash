from django.db import models
from user_accounts.models import CustomUser as User

class WashStation(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='washstation')
    name = models.CharField(max_length=200)
    adress = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default= True)

    def __str__(self):
        return self.name
    
class Employee(models.Model):
    wash_id = models.ForeignKey(WashStation, on_delete=models.CASCADE, related_name="employee")
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return self.name
    
class Service(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    wash_id = models.ForeignKey(WashStation, on_delete=models.CASCADE, related_name='service')

    def __str__(self):
        return self.name
    
class Car(models.Model):
    wash_id = models.ForeignKey(WashStation, on_delete=models.CASCADE, related_name='car')
    service_id = models.ForeignKey(Service, on_delete=models.CASCADE)
    employe_id = models.ForeignKey(Employee, on_delete=models.CASCADE)
    car_model = models.CharField(max_length=100)
    car_number = models.CharField(max_length=10)
    entry_time = models.DateTimeField()
    exit_time = models.DateTimeField()

    def __str__(self):
        return f"{self.car_model} ({self.car_number})"

