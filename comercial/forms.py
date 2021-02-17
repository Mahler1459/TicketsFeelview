from django import forms

class busquedaSimpleForm(forms.Form):
	nombre = forms.CharField(label='Nombre', max_length=100, required=False)
	direccion = forms.CharField(label='Dirección', max_length=100)
	ciudad = forms.CharField(label='Ciudad', max_length=100)
	provincia = forms.CharField(label='Provincia', max_length=100, required=False)
	radio = forms.IntegerField(label='Radio', max_value=30000, initial=1500)