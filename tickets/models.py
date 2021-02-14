from django.db import models
'''
class Cajero(models.Model):
	NroSerie = models.CharField(max_length=30)
	Numero = models.CharField(max_length=10)
'''
class Ticket(models.Model):
	#Terminal = models.ForeignKey(Cajero, on_delete=models.CASCADE)
	Terminal = models.CharField(max_length=20)
	Fecha = models.CharField(max_length=20)
	Hora = models.CharField(max_length=20)
	Evento = models.CharField(max_length=50)
	Locacion = models.CharField(max_length=50)
	EntryID = models.CharField(max_length=300)
	Status = models.CharField(max_length=20, default="SIN_STATUS")