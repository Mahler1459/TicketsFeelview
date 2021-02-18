from django import forms

CHOICES = (('Reciclador', 'Reciclador',), ('Dispensador', 'Dispensador',))

class busquedaSimpleForm(forms.Form):
	nombre = forms.CharField(label='Nombre', max_length=100, required=False)
	direccion = forms.CharField(label='Dirección', max_length=100)
	ciudad = forms.CharField(label='Ciudad', max_length=100)
	provincia = forms.CharField(label='Provincia', max_length=100, required=False)
	#radio = forms.ChoiceField(widget=forms.Select, choices=CHOICES)
	radio = forms.IntegerField(label='Radio', max_value=15000, initial=3000)

class simulacionSimpleForm(forms.Form):
	transacciones = forms.IntegerField(label='Tx Promedio Cajero')
	#cajero = forms.CharField(label='Tipo de Cajero', max_length=40)
	cajero = forms.ChoiceField(label = 'Tipo de Cajero',widget=forms.Select, choices=CHOICES)
