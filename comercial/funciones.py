from requests import get
from urllib.parse import urlencode
from gmplot import GoogleMapPlotter
from shapefile import Reader
from shapely.geometry import Polygon
from statistics import median
from math import sin, cos, atan2, sqrt, pi
from pyproj import Transformer, CRS

#path = '/home/dr/ticketsFeelview/comercial/Radios/'
path = 'C:\\Users\\agust\\Desktop\\Octagon\\ticketsFeelview/comercial/Radios/'

api_key = "AIzaSyBXug68S-1xipO5CFnaX5rVw4XygUxPX54"

provincias = {
	'Provincia de Buenos Aires':'Buenos_Aires_con_datos',
	'Buenos Aires Province':'Buenos_Aires_con_datos',
	'Buenos Aires':'CABA_con_datos',
	'Catamarca':'Catamarca_con_datos',
	'Chaco':'Chaco_con_datos',
	'Chubut':'Chubut_con_datos',
	'Cordoba':'Cordoba_con_datos',
	'Córdoba':'Cordoba_con_datos',
	'Corrientes':'Corrientes_con_datos',
	'Entre Rios':'Entre_Ríos_con_datos',
	'Entre Ríos':'Entre_Ríos_con_datos',
	'Formosa':'Formosa_con_datos',
	'Jujuy':'Jujuy_con_datos',
	'La Pampa':'La_Pampa_con_datos',
	'La Rioja':'La_Rioja_con_datos',
	'Mendoza':'Mendoza_con_datos',
	'Misiones':'Misiones_con_datos',
	'Neuquén':'Neuquen_con_datos',
	'Neuquen':'Neuquen_con_datos',
	'Río Negro':'Rio_Negro_con_datos',
	'Rio Negro':'Rio_Negro_con_datos',
	'Salta':'Salta_con_datos',
	'San Juan':'San_Juan_con_datos',
	'San Luis':'San_Luis_con_datos',
	'San Luis Province':'San_Luis_con_datos',
	'Santa Cruz':'Santa_Cruz_con_datos',
	'Santa Fe':'Santa_Fe_con_datos',
	'Santiago del Estero':'Santiago_del_Estero_con_datos',
	'Tierra del Fuego':'Tierra_del_Fuego_con_datos',
	'Tucumán':'Tucuman_con_datos',
	'Tucuman':'Tucuman_con_datos'
}

#me da el dato de la locacion que quiero buscar
def extract_lat_lng(address_or_postal, api_key):
	num, calle, loc, prov = '','','',''
	data_type = "json"
	endpoint = f"https://maps.googleapis.com/maps/api/geocode/{data_type}"
	params = {"address": address_or_postal, "key": api_key, "components": "country:AR"}
	url_params = urlencode(params)
	url = f"{endpoint}?{url_params}"
	r = get(url)
	if r.status_code not in range (200, 299):
		return {}
	latlng = {}
	try:
		latlng = r.json()['results'][0]['geometry']['location']
	except:
		pass
	response = {'num':'','calle':'loc','prov':''}
	for a in r.json()['results'][0]['address_components']:
		if 'street_number' in a['types']:
			response['num'] = a['long_name']
		if 'route' in a['types']:
			response['calle'] = a['long_name']
		if 'administrative_area_level_2' in a['types']:
			response['loc'] = a['long_name']
		if 'administrative_area_level_1' in a['types']:
			response['prov'] = a['long_name']
			response['lat'] = latlng.get("lat")
			response['lng'] = latlng.get("lng")
			response['formated'] = r.json()['results'][0]['formatted_address']
	return response

def getNearby(keywords, lat, lng, radio, keyTypes):
	places_endpoint_2 = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
	cajeros = []
	for keyword in keywords:
		params_2 = {
		"key": api_key,
		"keyword": keyword,
		"location": f"{lat},{lng}",
		"radius": radio,
		"rankBy": "distance"
		}
		params_2_encoded = urlencode(params_2)
		places_url = f"{places_endpoint_2}?{params_2_encoded}"

		r2 = get(places_url)
		c = r2.json()['results']
		coord = getCoord(cajeros)
		for cajero in c:
			if keyTypes:
				if not cajero['geometry']['location']['lat'] in coord and [i for i in keyTypes if i in cajero['types']]:
					cajeros.append((cajero['geometry']['location']['lat'],cajero['geometry']['location']['lng']))
			else:    
				if not cajero['geometry']['location']['lat'] in coord:
					cajeros.append((cajero['geometry']['location']['lat'],cajero['geometry']['location']['lng']))
	return cajeros

def getCoord(caje):
	coord = []
	for caj in caje:
		coord.append(caj[0])
	return coord

def distance(lat1, lng1, y1, y2,transformer):
	x1, x2 = transformer.transform(lat1, lng1)    
	a = sin((x1*pi/180-y1*pi/180)/2)**2 + \
	cos(x1*pi/180)*cos(y1*pi/180)*sin((y2*pi/180-x2*pi/180)/2)**2
	c = 2 * atan2(sqrt(a), sqrt(1-a))
	return 6371000*c
    
def radCensalCercano(RadEsquina, lat, lng, transformer, radio):
	if distance(RadEsquina[0], RadEsquina[1], lat, lng,transformer) < radio:
		return True
    
def radCoord(latlng,transformer):
	coord = []
	for elem in latlng:
		x1,x2=transformer.transform(elem[0], elem[1])
		coord.append((x1,x2))
	return coord

#Funciona Buenos Aires, Catamarca
def getRadioCensal(RADIOS, lat, lng, radio):
	radiosCensales = []
	pobl = []
	area = []
	isn2004=CRS("+proj=tmerc +lat_0=-90 +lon_0=-66 +k=1 +x_0=3500000 +y_0=0 +ellps=WGS84 +units=m +no_defs") 
	wgs84=CRS("EPSG:4326")
	transformer = Transformer.from_crs(isn2004, wgs84)
	for radCensal in RADIOS:
		if type(radCensal['geometry']['coordinates'][0][0]) == list:
			if radCensalCercano(radCensal['geometry']['coordinates'][0][0][0], lat, lng,transformer, radio):
				radiosCensales.append(radCoord(radCensal['geometry']['coordinates'][0][0],transformer))
				pobl.append(radCensal['properties']['totalpobl'])
				area.append(Polygon(radCensal['geometry']['coordinates'][0][0]).area)
		else:
			if radCensalCercano(radCensal['geometry']['coordinates'][0][0], lat, lng,transformer, radio):
				radiosCensales.append(radCoord(radCensal['geometry']['coordinates'][0],transformer))
				pobl.append(radCensal['properties']['totalpobl'])
				area.append(Polygon(radCensal['geometry']['coordinates'][0]).area)
	return radiosCensales, pobl, area

#Funciona CABA
def getRadioCensal2(RADIOS, lat, lng, radio):
	radiosCensales = []
	pobl = []
	area = []
	isn2004=CRS("+proj=tmerc +lat_0=-90 +lon_0=-66 +k=1 +x_0=3500000 +y_0=0 +ellps=WGS84 +units=m +no_defs") 
	wgs84=CRS("EPSG:4326")
	transformer = Transformer.from_crs(isn2004, wgs84)
	for radCensal in RADIOS:
		if type(radCensal['geometry']['coordinates'][0][0]) == list:
			if radCensalCercano(radCensal['geometry']['coordinates'][0][0][0], lat, lng,transformer, radio):
				radiosCensales.append(radCoord(radCensal['geometry']['coordinates'][0][0],transformer))
				pobl.append(radCensal['properties']['TOT_POB'])
				area.append(Polygon(radCensal['geometry']['coordinates'][0][0]).area)
		else:
			if radCensalCercano(radCensal['geometry']['coordinates'][0][0], lat, lng,transformer, radio):
				radiosCensales.append(radCoord(radCensal['geometry']['coordinates'][0],transformer))
			if radCensal['properties']['TOT_POB'] == None:
				pobl.append(0.0)
			else:
				pobl.append(radCensal['properties']['TOT_POB'])
			area.append(Polygon(radCensal['geometry']['coordinates'][0]).area)
	return radiosCensales, pobl, area

def miMain(direccion, radio, api_key):
    
	from requests import get
	from urllib.parse import urlencode
	from gmplot import GoogleMapPlotter
	from shapefile import Reader
	from shapely.geometry import Polygon
	from statistics import median
	from math import sin, cos, atan2, sqrt, pi
	from pyproj import Transformer, CRS
	res = extract_lat_lng(direccion, api_key)
	lat, lng = res['lat'],res['lng']
	num, calle, loc, prov = res['num'], res['calle'], res['loc'], res['prov']
	cajeros = getNearby(['atm', 'cajero'], lat, lng, radio, ['atm'])

	rapipagos = getNearby(['rapipago', 'pagofacil'], lat, lng, radio, [])
	estaciones_de_servicio = getNearby(['estacion de servicio'], lat, lng, radio, ['gas_station'])

	sf = Reader(f'{path}{provincias[prov]}.shp')
	sfJSON = sf.__geo_interface__['features'] #convertir a JSON, me quedo solo con los datos
	if prov == 'Buenos Aires':
		radCensalesCercanos, poblacion, area = getRadioCensal2(sfJSON, lat, lng, radio)
	else:
		radCensalesCercanos, poblacion, area = getRadioCensal(sfJSON, lat, lng, radio)
	pobTot = sum(poblacion)
	if len(cajeros)>0:
		habxcaj = int(pobTot/len(cajeros))
	else:
		habxcaj = 'N/A'
	data_locacion = {
		'NOMBRE DE SUCURSAL':f'{calle} {num}, {loc}', 
		'DIRECCIÓN':res['calle'],
		'LOCALIDAD':res['loc'],
		'PROVINCIA':res['prov'],
		'LATITUD y LONGITUD':f'{round(lat,7)},{round(lng,7)}',
		'POBLACION':int(pobTot),
		'CANTIDAD DE CAJEROS':len(cajeros),
		'HABITANTES POR CAJERO':int(habxcaj),
		'OPERACIONES POR CAJERO':int(habxcaj*0.5*0.6*3.5)
	}
	'''
	except:
		data_locacion = {
			'NOMBRE DE SUCURSAL':f'{calle} {num}, {loc}', 
			'DIRECCIÓN':'xxx',
			'LOCALIDAD':'xxx',
			'PROVINCIA':'xxx',
			'LATITUD y LONGITUD':'xxx',
			'POBLACION':'xxx',
			'CANTIDAD DE CAJEROS':'xxx',
			'HABITANTES POR CAJERO':'xxx'
		}
	'''
	# Creo el mapa
	gmap = GoogleMapPlotter(lat, lng, 15, apikey=api_key)

	for rapipago in rapipagos:
		gmap.marker(rapipago[0], rapipago[1], color='green')
	for estacion in estaciones_de_servicio:
		gmap.marker(estacion[0], estacion[1], color='orange')
	for cajero in cajeros:
		gmap.marker(cajero[0], cajero[1], color='blue')
	# Marco la locación
	gmap.marker(lat, lng, color='red')

	density = []
	for a, p in zip(area, poblacion):
		if p == None:
			density.append(0/a)
		else:
			density.append(p/a)

	med = int(median(density)*100000)
	maximun = int(max(density)*100000)
	minimun = int(min(density)*100000)
	med2 = int((maximun - minimun)/2)
	med = int(abs(med - med2)/2)
	paso1 = int((med - minimun)/3)
	paso2 = int((maximun - med)/3)
	for (rad, d) in zip(radCensalesCercanos,density):
		dens = int(d*100000)
		deita = zip(*rad)
		if dens in range(minimun,minimun+paso1):
			color = 'lemonchiffon'
		elif dens in range(minimun+paso1,minimun+2*paso1):
			color = 'khaki'
		elif dens in range(minimun+2*paso1,med):
			color = 'gold'
		elif dens in range(med,med+paso2):
			color = 'orange'
		elif dens in range(med+paso2,med+2*paso2):
			color = 'red'
		else:
			color = 'darkred'
		gmap.polygon(*deita, face_color=color, edge_width=1, face_alpha=0.5, edge_color='black', edge_alpha = 0.5)

	mapHTML = gmap.get()
	return mapHTML, data_locacion

def getServicioTecnico():

	gmap = GoogleMapPlotter(-33.876800, -64.611276, 6, apikey=api_key)

	servicioTecnicoList = [
		(-27.386631, -55.922307), #posadas
		(-27.459286, -58.985561), #resistencia
		(-27.484268, -58.819166), #corrientes
		(-31.417894, -64.188853), #cordoba
		(-32.953342, -60.670549), #rosario
		(-32.887442, -68.848220), #mendoza
		(-41.141376, -71.305771), #bariloche
		(-38.948785, -68.051566), #neuquen
		(-45.862832, -67.482980), #comodoro rivadavia
		(-36.622799, -64.291040), #santa rosa
		(-34.634315, -58.407165), #CABA
		(-38.024436, -57.555790), #Mar del Plata
		(-35.444645, -60.884653), #9 de Julio
	]

	for item in servicioTecnicoList:
		gmap.circle(item[0], item[1], 200000, edge_alpha=0, color='#cccccc')

	mapHTML = gmap.get()
	return mapHTML

def getSimulacion(transacciones, cajero):
	operaciones = {}
	comisiones = {}
	resultados = {}

	operaciones['Extracciones'] = int(transacciones*0.2)
	operaciones['Prestamos'] = int(transacciones*0.023)
	operaciones['Transferencias PtoP'] = int(transacciones*0.023)
	operaciones['Otras Liquidaciones'] = int(transacciones*0.012)
	operaciones['Pago de servicios'] = int(transacciones*0.018)
	operaciones['Pago de convenios'] = int(transacciones*0.018)
	operaciones['TOTAL'] = operaciones['Extracciones'] + operaciones['Prestamos'] + operaciones['Transferencias PtoP'] \
	+ operaciones['Otras Liquidaciones'] + 	operaciones['Pago de servicios'] + operaciones['Pago de convenios']

	comisiones['Extracciones'] = "$ 65"
	comisiones['Prestamos'] = "3%"
	comisiones['Transferencias PtoP'] = "$ 70"
	comisiones['Otras Liquidaciones'] = "2%"
	comisiones['Pago de servicios'] = "0,1%"
	comisiones['Pago de convenios'] = "0,3%"

	TotalAnual = 12 * (operaciones['Extracciones']*65 + operaciones['Prestamos']*20000*0.03 + \
		operaciones['Transferencias PtoP']*70 + operaciones['Otras Liquidaciones']*20000*0.02 + \
		operaciones['Pago de servicios']*15000*0.01 + operaciones['Pago de convenios']*15000*0.01)
	resultados['Cajero'] = TotalAnual
	resultados['Dueño'] = TotalAnual*0.2
	resultados['Establecimiento'] = TotalAnual*0.3
	resultados['Negocio Completo'] = TotalAnual*0.5
	return operaciones, comisiones, resultados