from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('datepicker/', views.datepicker, name='datepicker'),
]