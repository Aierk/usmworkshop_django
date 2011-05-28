# -*- coding: utf-8 -*-
from main.models import Perfil, SKILLS_CHOICES
from django import forms
from django.shortcuts import render_to_response

class RegistroForm(forms.Form):
	nombre = forms.CharField(max_length=20, required=True, initial='Tu Nombre.')
	apellido = forms.CharField(max_length=20, required=True, initial='Tu Apellido.')
	email = forms.EmailField(required=True,initial='Correo de contancto.')
	rut  = forms.CharField(max_length=10,required=True, initial='Con guiones y sin puntos.')
	fono = forms.CharField(max_length=15, required=True, initial='Telefono de contacto.')
	organizacion = forms.CharField(max_length=50),'Universidad u organización de origen.'
	notebook = forms.BooleanField(initial=False)
	equipo = forms.CharField(max_length=50)
	skill = forms.ChoiceField(choices=SKILLS_CHOICES, initial='n')



def Registro(request):
	if request.method == "POST":
		rform = RegistroForm(data == request.POST)
	else:
		rform = RegistroForm()
	return render_to_response('public/registro.html',{'form': rform}
