import json

#path = '/home/dr/ticketsFeelview/comercial/'
path = 'C:/Users/agust/Desktop/Octagon/ticketsFeelview/comercial/'

def getSimulacion2(transacciones, cajero, comercio):
	with open(f"{path}data.json", "r") as read_file:
		data = json.load(read_file)

	#print(data)
	#operaciones : cantidad de operaciones
	#comisiones : lo que se cobra en comisiones
	#
	#falta multiplicar por dispensador y reciclador
	nombres = data["nombres"]
	if cajero == 'Dispensador':
		operaciones = [int(transacciones * a * b * float(comercio)) for a,b in zip(data["porcentajes"],data["op_disp"])]
		comisiones = \
		[int(a*b*c) for a,b,c in zip(data["montos_com_disp"],data["comisiones_disp"],operaciones)]
		monto = data["montos_vault_disp"]
		interv = data["int_disp"]
		por = data["por_disp"]
		print("AAAA")
	else:
		operaciones = [int(transacciones * a * b * float(comercio)) for a,b in zip(data["porcentajes"],data["op_rec"])]
		comisiones = \
		[int(a*b*c) for a,b,c in zip(data["montos_com_rec"],data["comisiones_rec"],operaciones)]
		monto = data["montos_vault_rec"]
		interv = data["int_rec"]
		por = data["por_rec"]

	vault = "$ {:,}".format(int(sum([ m*op for m,op in zip(monto, operaciones)])/30)).replace(",",".")
	totalComisiones = sum(comisiones)
	totalOperaciones = sum(operaciones)
	monto = [abs(a) for a in monto]
	if totalOperaciones < interv[0]:
		mult = por[0]
	elif totalOperaciones > interv[0] and totalOperaciones < interv[1]:
		mult = por[1]
	else:
		mult = por[2]

	porcentaje = [round(a/totalComisiones*100,1) for a in comisiones]
	TotalAnual = 12*sum(comisiones)

	resultados = {}
	resultados['Inversor'] = 			"$ {:,}".format(int(TotalAnual*0.3)).replace(",",".")
	resultados['Establecimiento'] = 	"$ {:,}".format(int(TotalAnual*mult)).replace(",",".")
	resultados['Negocio Completo'] = 	"$ {:,}".format(int(TotalAnual*(0.3+mult))).replace(",",".")
	print(totalOperaciones)
	print(mult)
	print(interv)

	porNegocio = ["{:,}".format(int(100*0.3)).replace(",","."), "{:,}".format(int(100*mult)).replace(",","."), "{:,}".format(round(100*((0.3+mult)))).replace(",",".")]
	
	return operaciones, comisiones, resultados, nombres, "{:,}".format(totalOperaciones).replace(",","."),\
	 porNegocio, monto, porcentaje, "{:,}".format(totalComisiones).replace(",","."), vault