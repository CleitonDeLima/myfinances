import django_filters
from bootstrap_datepicker_plus import DatePickerInput
from taggit.managers import TaggableManager

from core import models


class RecordFilter(django_filters.FilterSet):
    start_date = django_filters.DateFilter(
        field_name='date',
        lookup_expr='gte',
        widget=DatePickerInput(format='%d/%m/%Y').start_of('between_date')
    )
    end_date = django_filters.DateFilter(
        field_name='date',
        lookup_expr='lte',
        widget=DatePickerInput(format='%d/%m/%Y').end_of('between_date')
    )

    class Meta:
        model = models.Record
        fields = ['start_date', 'end_date', 'bill', 'tags']
        filter_overrides = {
            TaggableManager: {
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'name__in',
                },
            },
        }
