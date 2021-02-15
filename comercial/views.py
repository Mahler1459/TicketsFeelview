from django.shortcuts import render
from django.http import HttpResponse
from .forms import busquedaSimpleForm

# Create your views here.
def home(request):
	return HttpResponse('<h1>COMERCIAL</h1>')

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
		return HttpResponseRedirect('/thanks/')

		# if a GET (or any other method) we'll create a blank form
	else:
		form = busquedaSimpleForm()

	return render(request, 'comercial/busqueda-simple.html', {'form': form})