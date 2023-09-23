from django.contrib import admin
from .models import Machine, Standard, MeasurementPoint, Report, Reading
# Register your models here.

admin.site.register(Machine)
admin.site.register(Standard)
admin.site.register(MeasurementPoint)
admin.site.register(Report)
admin.site.register(Reading)