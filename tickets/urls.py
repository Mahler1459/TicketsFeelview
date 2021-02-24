from django.urls import path
from . import views
import os

urlpatterns = [
	path('', views.index, name='index'),
	path('semaforo/', views.semaforo, name='semaforo'),
	path('semaforo/porcajero/<str:id>/', views.porCajero, name='por-cajero'),
	path('delete/<str:caj>/<str:eve>/', views.delete, name='delete')
]