from django.contrib import admin

from core import models


@admin.register(models.Bill)
class BillAdmin(admin.ModelAdmin):
    list_display = ['name', 'type']


@admin.register(models.Record)
class RecordAdmin(admin.ModelAdmin):
    list_display = ['type', 'value', 'date', 'bill', 'tag_list']
    list_filter = ['type', 'bill']
    ordering = ['-date']
