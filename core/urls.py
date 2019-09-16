from django.urls import path, include
from rest_framework import routers

from core import views

router = routers.DefaultRouter()
router.register('expenses', views.ExpenseViewSet, basename='expenses')
router.register('incomes', views.IncomeViewSet, basename='incomes')
router.register('categories', views.CategoryViewSet, basename='categories')
router.register('bills', views.BillViewSet, basename='bills')


urlpatterns = [
    path('', include(router.urls)),
]
