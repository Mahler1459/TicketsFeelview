from django import forms

class busquedaSimpleForm(forms.Form):
	nombre = forms.CharField(label='Nombre', max_length=100)
	direccion = forms.CharField(label='Dirección', max_length=100)
	ciudad = forms.CharField(label='Ciudad', max_length=100)
	provincia = forms.CharField(label='Provincia', max_length=100)
	radio = forms.CharField(label='Radio', max_length=100)