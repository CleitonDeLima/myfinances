from django.conf import settings
from django.contrib import admin
from django.urls import path, include

from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),

    path('', views.home, name='home'),
    path('contas/', include([
        path('', views.bill_list, name='bill-list'),
        path('nova/', views.bill_create, name='bill-create'),
        path('<uuid:pk>/atualizar/', views.bill_update, name='bill-update'),
    ])),

    path('despesas/', include([
        path('', views.expense_list, name='expense-list'),
        path('nova/', views.expense_create, name='expense-create'),
        path('<uuid:pk>/atualizar/', views.expense_update, name='expense-update'),
        path('<uuid:pk>/excluir/', views.expense_delete, name='expense-delete'),
    ])),

    path('receitas/', include([
        path('', views.income_list, name='income-list'),
        path('nova/', views.income_create, name='income-create'),
        path('<uuid:pk>/atualizar/', views.income_update, name='income-update'),
        path('<uuid:pk>/excluir/', views.income_delete, name='income-delete'),
    ])),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),

    ] + urlpatterns
