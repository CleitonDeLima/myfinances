from django.contrib import admin

from core import models


@admin.register(models.Bill)
class BillAdmin(admin.ModelAdmin):
    list_display = ['name', 'type']


@admin.register(models.Record)
class RecordAdmin(admin.ModelAdmin):
    list_display = ['type', 'value', 'date', 'category', 'bill']
    list_filter = ['type', 'category', 'bill']


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'type']
    list_filter = ['type']
