import django_filters
from .models import Complaint

class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Complaint
        fields = ['status','category']