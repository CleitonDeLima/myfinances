from django.contrib import admin

from core import models


@admin.register(models.Bill)
class BillAdmin(admin.ModelAdmin):
    list_display = ['name', 'type']


@admin.register(models.Record)
class RecordAdmin(admin.ModelAdmin):
    list_display = ['type', 'value', 'date', 'category', 'bill', 'tag_list']
    list_filter = ['type', 'category', 'bill']
    ordering = ['-date']


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'type']
    list_filter = ['type']
