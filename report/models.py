from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator 

class Machine(models.Model):
    name = models.CharField(max_length=30)
    def __str__(self) -> str:
        return self.name

class Standard(models.Model):
    name = models.CharField(max_length=30)
    threshold_1 = models.IntegerField()
    threshold_2 = models.IntegerField()

    def __str__(self) -> str:
        return self.name

class MeasurementPoint(models.Model):
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    standard = models.ForeignKey(Standard,on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Reading(models.Model) :  
    measurement_point = models.ForeignKey(MeasurementPoint, on_delete=models.CASCADE)  
    x_point = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    y_point = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    z_point = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    x_severity = models.CharField(max_length=10)
    y_severity = models.CharField(max_length=10)
    z_severity = models.CharField(max_length=10)

class Report(models.Model):
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    overall_severity = models.CharField(
        max_length=10
    )
    results = models.ManyToManyField(Reading)
    remarks = models.TextField(null=True)
    def __str__(self) -> str:
        return f'{self.machine.name} - {self.date}'





