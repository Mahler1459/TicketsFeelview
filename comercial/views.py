from django.shortcuts import render
from django.http import HttpResponse
from .forms import busquedaSimpleForm
from .funciones import miMain, getServicioTecnico

# Create your views here.
def home(request):
	return render(request, 'comercial/comercial-home.html')

def busquedaSimple(request):
	# if this is a POST request we need to process the form data
	if request.method == 'POST':
		# create a form instance and populate it with data from the request:
		form = busquedaSimpleForm(request.POST)
		# check whether it's valid:
		if form.is_valid():	
			#acá tengo que hacer todo para leer el mapa
			nombre = form.cleaned_data['nombre']
			direccion = form.cleaned_data['direccion']
			ciudad = form.cleaned_data['ciudad']
			provincia = form.cleaned_data['provincia']
			radio = form.cleaned_data['radio']
			
			print(form.cleaned_data)

			api_key = "AIzaSyBXug68S-1xipO5CFnaX5rVw4XygUxPX54"
			
			mapHTML, data_locacion = miMain(f'{direccion} {ciudad}', radio, api_key)

			print(data_locacion)
		return render(request, 'comercial/busqueda-simple-resultado.html', {'mapa': mapHTML[7:-9], 'data':data_locacion})

		# if a GET (or any other method) we'll create a blank form
	else:
		form = busquedaSimpleForm()

	return render(request, 'comercial/busqueda-simple.html', {'form': form})

def servicioTecnico(request):
	mapHTML = getServicioTecnico()
	return render(request, 'comercial/servicio-tecnico.html', {'mapa': mapHTML[7:-9]})