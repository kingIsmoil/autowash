import django_filters
from .models import Car

class CarFilter(django_filters.FilterSet):
    entry_time__gte = django_filters.DateTimeFilter(field_name='entry_time', lookup_expr='gte')
    entry_time__lte = django_filters.DateTimeFilter(field_name='entry_time', lookup_expr='lte')

    class Meta:
        model = Car
        fields = ['entry_time__gte', 'entry_time__lte']
