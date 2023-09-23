from django import forms
from .models import Machine, Standard, MeasurementPoint, Report, Reading

class ReadingForm(forms.ModelForm):

    class Meta :
        model = Reading
        fields = ['x_point','y_point','z_point']

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['remarks']
