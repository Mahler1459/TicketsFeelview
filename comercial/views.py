from django.core import serializers
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .forms import busquedaSimpleForm, simulacionSimpleForm
from .funciones import miMain, getServicioTecnico
from .simulacion import getSimulacion2
import json
# Create your views here.
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt

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
			direccion = form.cleaned_data['direccion']
			ciudad = form.cleaned_data['ciudad']
			provincia = form.cleaned_data['provincia']
			radio = form.cleaned_data['radio']
			api_key = "AIzaSyBXug68S-1xipO5CFnaX5rVw4XygUxPX54"
			mapHTML, data_locacion = miMain(f'{direccion} {ciudad}', radio, api_key)

		opxcaj = data_locacion['OPERACIONES POR CAJERO']
		if opxcaj == 'N/A':
			opxcaj = 1000
		form = simulacionSimpleForm(initial={'transacciones':int(opxcaj*0.2)})
		return render(request, 'comercial/busqueda-simple-resultado.html', {'mapa': mapHTML[7:-9], 'data':data_locacion, 'form':form})
		# if a GET (or any other method) we'll create a blank form
	else:
		form = busquedaSimpleForm()
	return render(request, 'comercial/busqueda-simple.html', {'form': form})

def servicioTecnico(request):
	mapHTML = getServicioTecnico()
	return render(request, 'comercial/servicio-tecnico.html', {'mapa': mapHTML[7:-9]})

def simulacionSimple(request):
	if request.method == 'POST':
		form = simulacionSimpleForm(request.POST)
		return render(request, 'comercial/comercial-home.html')
	else:
		form = simulacionSimpleForm()
	return render(request, 'comercial/simulacion-simple.html', {'form': form})

def postCalculo(request):
	# request should be ajax and method should be POST.
	if request.is_ajax and request.method == "POST":
	# get the form data
		form = simulacionSimpleForm(request.POST)
	# save the data and after fetch the object in instance
		if form.is_valid():
			operaciones, comisiones, resultados, nombres, totalOperaciones, porNegocio, monto, porcentajes, totalComisiones,\
			vault = getSimulacion2(form.cleaned_data['transacciones'],form.cleaned_data['cajero'],form.cleaned_data['comercio'])

			op = ["{:,}".format(a).replace(",",".") for a in operaciones]
			com = ["{:,}".format(a).replace(",",".") for a in comisiones]
			mon = ["{:,}".format(a).replace(",",".") for a in monto]
			# serialize in new friend object in json
			ser_instance = json.dumps([com, op, resultados, nombres, totalOperaciones, \
				porNegocio, mon, porcentajes, totalComisiones, vault])
			# send to client side.
			return JsonResponse({"instance": ser_instance}, status=200)
		else:
			print("error")
		# some form errors occured.
			return JsonResponse({"error": form.errors}, status=400)
	# some error occured
	return JsonResponse({"error": ""}, status=400)


def testposteo(request):
	# if this is a POST request we need to process the form data
	if request.method == 'POST':
		# create a form instance and populate it with data from the request:
		print((request.POST["value"]))
		a = request.POST["value"]
		if barcode == asdasdasdasda:
			return JsonResponse({"respuesta":"OK","dato":a}, status=200)
		return HttpResponse({"respuesta":"OK","dato":a})
	else:
		return HttpResponse("Hola, hiciste un GET")