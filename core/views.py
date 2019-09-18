from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from core.models import Record, Category, Bill
from core.serializers import (
    ExpenseSerializer, IncomeSerializer, CategorySerializer, BillSerializer
)


class ExpenseViewSet(viewsets.ModelViewSet):
    serializer_class = ExpenseSerializer
    queryset = Record.objects.filter(type=Record.OUT).order_by('-created_at')


class IncomeViewSet(viewsets.ModelViewSet):
    serializer_class = IncomeSerializer
    queryset = Record.objects.filter(type=Record.IN).order_by('-created_at')


class CategoryViewSet(mixins.CreateModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.ListModelMixin,
                      mixins.RetrieveModelMixin,
                      viewsets.GenericViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class BillViewSet(mixins.CreateModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):
    serializer_class = BillSerializer
    queryset = Bill.objects.all()

    @action(detail=False)
    def balance(self, request, pk=None):
        queryset = self.get_queryset().balance()
        data = [
            dict(
                id=b.id,
                name=b.name,
                expense_count=b.expense_count,
                income_count=b.income_count,
                balance=b.balance
            )
            for b in queryset
        ]

        return Response(data)
