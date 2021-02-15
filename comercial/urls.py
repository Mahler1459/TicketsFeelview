from django.urls import path
from . import views
import os

urlpatterns = [
	path('', views.home, name='home'),
	path('busqueda-simple/', views.busquedaSimple, name='busqueda-simple'),
]