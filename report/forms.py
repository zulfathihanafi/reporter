from typing import Any
from django import forms
from .models import Machine, Standard, MeasurementPoint, Report, Reading
from django.core.exceptions import ValidationError

class ReadingForm(forms.ModelForm):

    x_point = forms.IntegerField(required=True)
    class Meta :
        model = Reading
        fields = ['x_point','y_point','z_point']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['x_point'].widget.attrs.update({'required': ''})
        self.fields['y_point'].widget.attrs.update({'required': ''})
        self.fields['z_point'].widget.attrs.update({'required': ''})
    
class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['remarks']
