from django.urls import path, include

from core import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('contas/', views.bill_list, name='bill-list'),

    path('despesas/', include([
        path('', views.expense_list, name='expense-list'),
        path('novo/', views.expense_create, name='expense-create'),
    ])),

    path('receitas/', include([
        path('', views.income_list, name='income-list'),
        path('novo/', views.income_create, name='income-create'),
    ])),

    path('<uuid:pk>/excluir/', views.record_delete, name='record-delete'),
]
