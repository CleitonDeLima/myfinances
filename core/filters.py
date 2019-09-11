import django_filters

from core import models


class RecordFilter(django_filters.FilterSet):
    class Meta:
        model = models.Record
        fields = ['date', 'category', 'bill']
