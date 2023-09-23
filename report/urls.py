from django.urls import path

from . import views

urlpatterns = [
    # Home page
    path('', views.index, name='index'),
    path('machine/<int:pk>', views.machine_details, name='machine_details'),
    path('report/', views.report, name='report'),
    path('report/create', views.report_create, name='report_create'),
    path('report/<int:pk>', views.report_details, name='report_details'),
]