import json

#path = '/home/dr/ticketsFeelview/comercial/Radios/'
path = 'C:/Users/agust/Desktop/Octagon/ticketsFeelview/comercial/'

def getSimulacion2(transacciones, cajero):
	with open(f"{path}data.json", "r") as read_file:
		data = json.load(read_file)

	print(data)
	operaciones = {}
	comisiones = {}
	resultados = {}
	
	operaciones['extracciones'] = int(transacciones*0.2)
	operaciones['prestamos'] = int(transacciones*0.023)
	operaciones['envio'] = int(transacciones*0.023)
	operaciones['otrliq'] = int(transacciones*0.012)
	operaciones['pserv'] = int(transacciones*0.018)
	operaciones['pcomv'] = int(transacciones*0.018)

	operaciones['TOTAL'] = operaciones['extracciones'] + \
		operaciones['prestamos'] + operaciones['envio'] + \
		operaciones['otrliq'] + operaciones['pserv'] + operaciones['pcomv']

	comisiones['extracciones'] = f"$ {data['comisiones']['extracciones']}"
	comisiones['prestamos'] = f"{data['comisiones']['prestamos']} %"
	comisiones['envio'] = f"$ {data['comisiones']['envio']}"
	comisiones['otrliq'] = f"{data['comisiones']['otrliq']} %"
	comisiones['pserv'] = f"{data['comisiones']['pserv']} %"
	comisiones['pcomv'] = f"{data['comisiones']['pconv']} %"

	TotalAnual = 12 * (operaciones['Extracciones']*data['comisiones']['extracciones'] + \
		operaciones['prestamos']*data['monto']['prestamos']*data['comisiones']['prestamos'] + \
		operaciones['envio']*data['comisiones']['envio'] + \
		operaciones['otrliq']*data['monto']['otrliq']*data['comisiones']['otrliq'] + \
		operaciones['pserv']*data['monto']['pserv']*data['comisiones']['pserv'] + \
		operaciones['Pago de convenios']*data['monto']['pconv']*data['comisiones']['pserv'])
	
	resultados['Cajero'] = TotalAnual
	resultados['Dueño'] = TotalAnual*0.2
	resultados['Establecimiento'] = TotalAnual*0.3
	resultados['Negocio Completo'] = TotalAnual*0.5
	return operaciones, comisiones, resultados