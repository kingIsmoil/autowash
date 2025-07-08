import django_filters
from .models import Car

class CarFilter(django_filters.FilterSet):
    entry_time = django_filters.DateFromToRangeFilter()
    exit_time = django_filters.DateFromToRangeFilter()

    class Meta:
        model = Car
        fields = ['entry_time', 'exit_time', 'employe_id', 'wash_id']
