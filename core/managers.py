from django.db.models import QuerySet, Sum, Value, Count, Q
from django.db.models.functions import Coalesce


class BillQuerySet(QuerySet):

    def balance(self):
        IN = '1'
        OUT = '2'
        sum_in = Coalesce(
            Sum('records__value', filter=Q(records__type=IN)),
            Value(0)
        )
        sum_out = Coalesce(
            Sum('records__value', filter=Q(records__type=OUT)),
            Value(0)
        )
        count_in = Count('records', filter=Q(records__type=IN))
        count_out = Count('records', filter=Q(records__type=OUT))

        return self.annotate(
            expense_count=count_out,
            income_count=count_in,
            balance=sum_in - sum_out
        )
