from django import forms

CAJERO_CHOICES = (('Reciclador', 'Reciclador',), ('Dispensador', 'Dispensador',))
COMERCIO_CHOICES = ((0.3,'Grande',), (0.25,'Mediano',), (0.2,'Chico',))
class busquedaSimpleForm(forms.Form):
	direccion = forms.CharField(label='Dirección', max_length=100)
	ciudad = forms.CharField(label='Ciudad', max_length=100)
	provincia = forms.CharField(label='Provincia', max_length=100, required=False)
	#radio = forms.ChoiceField(widget=forms.Select, choices=CHOICES)
	radio = forms.IntegerField(label='Radio', max_value=15000, initial=1500)

class simulacionSimpleForm(forms.Form):
	transacciones = forms.IntegerField(label='Extracciones Promedio Cajero')
	#cajero = forms.CharField(label='Tipo de Cajero', max_length=40)
	cajero = forms.ChoiceField(label = 'Tipo de Cajero',widget=forms.Select, choices = CAJERO_CHOICES)
	comercio = forms.ChoiceField(label = 'Tipo de Comercio',widget=forms.Select, choices = COMERCIO_CHOICES)