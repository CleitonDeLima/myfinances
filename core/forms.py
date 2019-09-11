from django import forms

from core import models


class RecordForm(forms.ModelForm):
    class Meta:
        model = models.Record
        fields = [
            'value', 'date', 'description', 'category', 'bill', 'observation'
        ]
