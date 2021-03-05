import json

#path = '/home/dr/ticketsFeelview/comercial/'
path = 'C:/Users/agust/Desktop/Octagon/ticketsFeelview/comercial/'

def getSimulacion2(transacciones, cajero):
	with open(f"{path}data.json", "r") as read_file:
		data = json.load(read_file)

	#print(data)
	#operaciones : cantidad de operaciones
	#comisiones : lo que se cobra en comisiones
	#
	#falta multiplicar por dispensador y reciclador

	nombres = data["nombres"]
	if cajero == 'Dispensador':
		operaciones = [int(transacciones * a * b) for a,b in zip(data["porcentajes"],data["op_disp"])]
		comisiones = \
		[int(a*b*c) for a,b,c in zip(data["montos_com_disp"],data["comisiones_disp"],operaciones)]
		monto = data["montos_vault_disp"]
	else:
		operaciones = [int(transacciones * a * b) for a,b in zip(data["porcentajes"],data["op_rec"])]
		comisiones = \
		[int(a*b*c) for a,b,c in zip(data["montos_com_rec"],data["comisiones_rec"],operaciones)]
		monto = data["montos_vault_rec"]

	vault = "$ {:,}".format(sum([ m*op for m,op in zip(monto, operaciones)])).replace(",",".")
	totalComisiones = sum(comisiones)
	totalOperaciones = sum(operaciones)
	porcentaje = [round(a/totalComisiones*100,1) for a in comisiones]
	TotalAnual = 12*sum(comisiones)

	resultados = {}
	resultados['Inversor'] = "$ {:,}".format(int(TotalAnual*0.3)).replace(",",".")
	resultados['Establecimiento'] = "$ {:,}".format(int(TotalAnual*0.2)).replace(",",".")
	resultados['Negocio Completo'] = "$ {:,}".format(int(TotalAnual*0.5)).replace(",",".")
	
	return operaciones, comisiones, resultados, nombres, "{:,}".format(totalOperaciones).replace(",","."),\
	 data["porNegocio"], monto, porcentaje, "{:,}".format(totalComisiones).replace(",","."), vault