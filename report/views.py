from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Machine, Standard, MeasurementPoint, Report, Reading
from .forms import ReadingForm, ReportForm
from django import forms
from django.contrib import messages
# Create your views here.
def index(request):
    context = {
        'machines': Machine.objects.all()
    }
    print(context)
    return render(request, 'report/index.html', context)

def report(request):
    context = {
        'reports' : Report.objects.all()
    }
    
    return render(request, 'report/report.html', context)

def report_details(request, pk):
    context = { 
        'report' : Report.objects.get(pk = pk)
    }
    print(context['report'].date)
    return render(request, 'report/report_details.html', context)

def machine_details(request, pk):
    
    context= {
        'reports' : Report.objects.filter(machine = pk),
        'machine' : Machine.objects.get(pk = pk),
        'name' : 'Test'
    }
    return render(request, 'report/machine_details.html', context=context)

# def report_create(request):
#     if request.method == "POST":
#         form = ReadingForm(request.POST)
#         if form.is_valid():
#             print(form)
#             # instance = form.save()
#             # messages.success(request, "Your tag had been created")
#             return redirect('report')
#         else:
#             pass
#             # messages.error("Please correct the error below")
#     else:
#         pass
#         form = ReadingForm()
#     machine_id = request.GET['machine_id']
#     context ={
#         'machine' : Machine.objects.get(pk = machine_id),
#         'measurement_points' : MeasurementPoint.objects.filter(machine = machine_id),
#         'form' : ReadingForm()
#     }
#     # for content in context['measurement_points']:
#     #     print(content.standard.threshold_1)
    
#     return render(request, 'report/create_report.html',context=context)

def report_create(request):
    
    if request.method == 'POST':
        machine_id = request.GET['machine_id']
        measurementPoints = MeasurementPoint.objects.filter(machine = machine_id)
        print(measurementPoints)
        ReadingFormSet = forms.formset_factory(ReadingForm, extra=measurementPoints.count())
        report_form = ReportForm(request.POST)
        reading_formset = ReadingFormSet(request.POST)

        

        if report_form.is_valid() and reading_formset.is_valid():
            # Save the report
            # report = report_form.save()
            # # Link the readings to the report
            # saved_reading_ids = []
            index = 0
            readingsArray = []
            overallSeverityIndex = 0
            # Saving readings
            
            for reading_form in reading_formset:
                currentMeasurementPoint =  MeasurementPoint.objects.get(pk = measurementPoints[index].id)

                reading = Reading()
                reading.measurement_point = currentMeasurementPoint
                reading.x_point = reading_form.cleaned_data['x_point']
                reading.y_point = reading_form.cleaned_data['y_point']
                reading.z_point = reading_form.cleaned_data['z_point']

                currentThreshold1 = currentMeasurementPoint.standard.threshold_1
                currentThreshold2 = currentMeasurementPoint.standard.threshold_2

                severityLevel = ['Safe','Harm','Danger']
                

                def severityComparator(reading):
                    toReturnValue = 0
                    if reading < currentThreshold1:
                        toReturnValue = 0
                    else :
                        if reading < currentThreshold2:
                            toReturnValue = 1
                        else :
                            toReturnValue = 2
                    
                    print(toReturnValue)
                    return toReturnValue
                
                x_severity_value = severityComparator(reading_form.cleaned_data['x_point'])
                y_severity_value = severityComparator(reading_form.cleaned_data['y_point'])
                z_severity_value = severityComparator(reading_form.cleaned_data['z_point'])
                reading.x_severity = severityLevel[x_severity_value]
                reading.y_severity = severityLevel[y_severity_value]
                reading.z_severity = severityLevel[z_severity_value]

                overallSeverityIndex = max([overallSeverityIndex, x_severity_value, y_severity_value, z_severity_value])

                reading.save()
                readingsArray.append(reading)
                index+=1

            # Save report to get ID first     
            print('Current', severityLevel[overallSeverityIndex])       
            report = Report()
            report.machine = Machine.objects.get(pk = machine_id)
            report.overall_severity = severityLevel[overallSeverityIndex]
            report.remarks = report_form.cleaned_data['remarks']
            report.save()

            # # Save the results field (many to many)
            for data in readingsArray:
                report.results.add(data)
            report.save()

            messages.success(request, "Your series had been created")
            #     if reading_form.is_valid():
            #         reading = reading_form.save(commit=False)
            #         reading.report = report
            #         reading.save()
            #         saved_reading_ids.append(reading.id)
            
            return redirect('report_details', report.id)  # Redirect to a success page
        else :
            messages.error("Please correct the error below")
    else:
        machine_id = request.GET['machine_id']
        context = {
            'machine' : Machine.objects.get(pk = machine_id),
            'measurement_points' : MeasurementPoint.objects.filter(machine = machine_id),
            'report_form' : ReportForm(),
            'reading_formset' : forms.formset_factory(ReadingForm, extra=MeasurementPoint.objects.filter(machine = machine_id).count())
        }
        return render(request, 'report/create_report.html', context)
