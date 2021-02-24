from django.shortcuts import render
from django.http import HttpResponse
from tickets.models import Ticket 
from django.shortcuts import redirect

import smtplib
import time
import imaplib
import email
import traceback 

def index(request):

	return HttpResponse("Hello, world. You're at the polls index.")

def porCajero(request,id):
	data = []
	for item in Ticket.objects.filter(Terminal=id):
		temp=[]
		temp.append(item.Terminal)
		temp.append(item.Fecha)
		temp.append(item.Hora)
		temp.append(item.Evento)
		temp.append(item.Locacion)
		data.append(temp)
	return  render(request, 'tickets/porcajero.html',{'data': data})
	#return  render(request, 'tickets/por-cajero.html',{'normal': normal})

def delete(request,caj,eve):
	tick = Ticket.objects.filter(Terminal=caj, Status="ALERTA", Evento=eve)
	for ticketBaja in tick:
		ticketBaja.Status="ELIMINADO"
		ticketBaja.save()
	return redirect('/semaforo/')

def bajarTick(item):
	item.Status="BAJA"
	item.save()

def semaforo(request):
	getTheMails()
	################PREPARO PARA MANDAR
	error=[]
	warning=[]
	normal=[]

	warningList = ['Carbinet door (panel superior)', 'Poco Papel en Impresora', 'Sin Papel en Impresora',\
	 'Boveda Abierta', 'Pocos Billetes en Casetera', 'Panel Superior Abierto', 'Modo de Mantenimiento']

	errorList = ['Error de Panel Superior', 'Error de Impresora', 'Atasco de Papel en Impresora', \
	'Safe Door (boveda)', 'Error de Bóveda', 'Sin Billetes en Casetera', 'Error de Caseteras','Terminal sin conexion', \
	'Terminal parada', 'Error de sensores', 'Error de camara', 'Error de comunicacion', 'Error sensor proximidad', \
	'Error de camara alta', 'Error de Teclado']

	for item in Ticket.objects.filter(Status="ALERTA"):
		if item.Evento in errorList:
			temp=[]
			temp.append(item.Terminal)
			temp.append(item.Fecha)
			temp.append(item.Hora)
			temp.append(item.Evento)
			temp.append(item.Locacion)
			error.append(temp)
		elif item.Evento in warningList:
			temp=[]
			temp.append(item.Terminal)
			temp.append(item.Fecha)
			temp.append(item.Hora)
			temp.append(item.Evento)
			temp.append(item.Locacion)
			warning.append(temp)
		else:
			temp=[]
			temp.append(item.Terminal)
			temp.append(item.Fecha)
			temp.append(item.Hora)
			temp.append(item.Evento)
			temp.append(item.Locacion)
			normal.append(temp)

	return  render(request, 'tickets/semaforo.html',{'normal': normal, 'error': error, 'warning': warning})

#############GMAIL
def getTheMails():
	items=getMails()
	parsedItems=[]
	for item in items:
		parsed=parseMail(item["Subject"])
		parsedItems.append(parsed)

	for item in parsedItems:
		#si el ticket es normal bajo el correspondiente
		if item["Status"]=="NORMAL":
			tick = Ticket.objects.filter(Terminal=item["Terminal"], Status="ALERTA", Evento=item["Evento"][0])
			for ticket in tick:
				bajarTick(ticket)
		#caso alerta
		elif item["Status"]=="ALERTA":
			#me fijo si el alerta existe para cada evento
			for evento in item["Evento"]:
				tick=Ticket.objects.filter(Terminal=item["Terminal"], Status="ALERTA", Evento=evento)
				#si no encuento ningún alerta, lo cargo
				if not tick:
					createTick(item, "ALERTA", evento)
			#buscar si alguno ya está bajo pero no me llegó el alerta
			tick=Ticket.objects.filter(Terminal=item["Terminal"], Status="ALERTA")
			for ticket in tick:
				if ticket.Evento not in item["Evento"]:
					bajarTick(ticket)

	return redirect('/semaforo/')

def createTick(ticket, el_status, el_evento):
	newTicket = Ticket(Terminal=ticket["Terminal"],Fecha=ticket["Fecha"],Hora=ticket["Hora"],\
		Evento=el_evento,Locacion=ticket["Locacion"],Status=el_status)
	newTicket.save()
	return

def bajarTick(item):
	item.Status="BAJA"
	item.save()

def getMails():
	items = []
	ORG_EMAIL   = "@gmail.com"
	FROM_EMAIL  = "ticketsfeelview" + ORG_EMAIL
	FROM_PWD    = "Octag@n2020"
	SMTP_SERVER = "imap.gmail.com"
	SMTP_PORT   = 993

	mail = imaplib.IMAP4_SSL(SMTP_SERVER)
	mail.login(FROM_EMAIL,FROM_PWD)
	mail.select('inbox')
	data = mail.search(None, 'ALL')
	mail_ids = data[1]
	id_list = mail_ids[0].split()
	first_email_id = int(id_list[0])
	latest_email_id = int(id_list[-1])
	for i in range(latest_email_id,first_email_id, -1):
		data = mail.fetch(str(i), '(RFC822)' )
		for response_part in data:
			arr = response_part[0]
			if isinstance(arr, tuple):
				msg = email.message_from_string(str(arr[1],'iso-8859-1'))
				#msg = email.message_from_bytes(arr[1])
				email_subject = msg['subject']
				email_from = msg['from'].split('<')[1].split('>')[0]
				#print('From : ' + email_from + '\n')
				mess = {}
				if email_from == "agustinderuschi@hotmail.com" or email_from == "feelview@octagon-ar.com" or email_from == "grgbanking.feelview6.2@gmail.com":
					print('From : ' + email_from + '\n')
					mess["Subject"] = email_subject.replace('\n','').replace('\r','')
					print('Subject : ' + mess["Subject"] + '\n')
					print(mess)
					items.append(mess)
		mail.store(str(i), "+FLAGS", "\\Deleted" )	
	return items
	
def parseMail(subject): #funcion que parsea un subject del mail de feelview
	#Terminal ID;72172888@ Hora;2020-08-31 16:57:02@ Evento;Panel Superior Abierto@ \
		#Locacion;Octagon SA PP 1131756789@ Tipo de terminal;GRGBANKING I21 ATM@ Status;ALERTA
	try:

		div=subject.split("//") #Aca tengo todos los campos separados
		parsedMail={}
		parsedMail["Terminal"]=div[0].split(";")[1]
		parsedMail["Fecha"]=div[1].split(";")[1].split(" ")[0]
		parsedMail["Hora"]=div[1].split(";")[1].split(" ")[1]
		parsedMail["Evento"]=div[2].split(";")[1].split(",")
		parsedMail["Locacion"]=div[3].split(";")[1]
		parsedMail["Status"]=div[5].split(";")[1]

		return parsedMail
	except:
		parsedMail={}
		parsedMail["Terminal"]="XX"
		parsedMail["Fecha"]="XX"
		parsedMail["Hora"]="XX"
		parsedMail["Evento"]="XX"
		parsedMail["Locacion"]="XX"
		parsedMail["Status"]="ALERTA"
		return parsedMail
