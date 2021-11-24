from django.urls import path
from . import views
import os

urlpatterns = [
	path('', views.home, name='home'),
	path('busqueda-simple/', views.busquedaSimple, name='busqueda-simple'),
	path('servicio-tecnico/', views.servicioTecnico, name='servicio-tecnico'),
	path('simulacion-simple/', views.simulacionSimple, name='simulacion-simple'),
	path('post/ajax/calculo/', views.postCalculo, name='post-calculo'),
	path('test/', views.testposteo, name='test'),
]