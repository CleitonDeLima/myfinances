from rest_framework import viewsets, mixins

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
