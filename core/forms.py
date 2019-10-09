from django import forms
from bootstrap_datepicker_plus import DatePickerInput

from core.models import Record


class RecordForm(forms.ModelForm):
    class Meta:
        model = Record
        fields = [
            'value', 'date', 'description', 'category', 'bill', 'observation',
            'tags'
        ]
        widgets = {
            'date': DatePickerInput(format='%d/%m/%Y'),
            'description': forms.Textarea(attrs={'rows': 2}),
            'observation': forms.Textarea(attrs={'rows': 2}),
        }
