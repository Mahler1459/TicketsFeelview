from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
	return HttpResponse('<h1>COMERCIAL</h1>')

def otraVista(request):
	return HttpResponse('<h1>COMERCIAL</h1>')