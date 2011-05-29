# -*- coding: utf-8 -*-
from main.models import Perfil, SKILLS_CHOICES
from django import forms
from django.http import HttpResponse
from django.template import Template,Context
from django.template.loader import get_template
from django.core.context_processors import csrf
from django.contrib.localflavor.cl.forms import CLRutField
from main.models import Perfil
from workshop.settings import DEPLOY_PATH
import os
import random
import string

#Utils
def CodeGen():
	return ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(5))
	
	
## --- Registro ---
class RegistroForm(forms.Form):
	nombre = forms.CharField(max_length=20, required=False, help_text='Tu Nombre.')
	apellido = forms.CharField(max_length=20, required=False, help_text='Tu Apellido.')
	email = forms.CharField(required=False, help_text='Correo de contancto.')
	rut  = forms.CharField(required=False, help_text='Con guion y sin puntos.')
	fono = forms.CharField(max_length=15, required=True, help_text='Telefono de contacto.')
	org = forms.CharField(max_length=50, label='Organización de origen', initial="Ninguno",required=False)
	equipo = forms.CharField(max_length=50, required=False, label='Nombre de tu equipo',initial="Ninguno", help_text="Si posees uno")
	skill = forms.ChoiceField(choices=SKILLS_CHOICES, initial='n',label='Habilidad principal', help_text="Que trabajo prefieres hacer?")
	notebook = forms.BooleanField(initial=False,required=False,label='Llevas tu propio PC?',help_text='Solo Laptos por favor.')
	
	def clean(self):
		data = self.cleaned_data
		# Nombre
		nombre = data.get("nombre")
		apellido = data.get("apellido")
		if not nombre or not apellido:
			raise forms.ValidationError("Nombre y Apellido son obligatorios")

		rut_given = data.get("rut")
		rvalidator = CLRutField()
		print rut_given
		try:
			a=rvalidator.clean(rut_given)
		except:
			raise forms.ValidationError("El Rut no es valido.")
		persona = Perfil.objects.filter(rut=rut_given)
		if persona.exists():
			raise forms.ValidationError("El Rut ingresado ya esta registrado.")

		#Email
		email_given = data.get("email")
		evalidator = forms.EmailField()
		try:
			evalidator.clean(email_given)
		except:
			raise forms.ValidationError("El correo ingresado no es valido.")
		persona = Perfil.objects.filter(email=email_given)
		if persona.exists():
			raise forms.ValidationError("El correo ingresado ya esta registrado.")

		return data

	def save(self):
		#Guardar
		data = self.cleaned_data
		nombre = data.get("nombre")
		apellido = data.get("apellido")
		rut = data.get("rut")
		fono = data.get("fono")
		email = data.get("email")
		organizacion = data.get("org")
		notebook = data.get("notebook")
		equipo = data.get("equipo")
		skill = data.get("skill")
		code = CodeGen()
		p = Perfil(nombre=nombre,apellido=apellido,rut=rut,fono=fono,organizacion=organizacion,notebook=notebook,equipo=equipo,skill=skill,code=code, email=email)
		p.save()

def Registro(request):
	if request.method == "POST":
		rform = RegistroForm(data=request.POST)
		if rform.is_valid():
			rform.save()
			persona = Perfil.objects.get(email=request.POST['email'])
			t = get_template('public/registro-done.html')
			c = Context({'persona': persona})
			return HttpResponse(t.render(c))
	else:
		rform = RegistroForm()

	t = get_template('public/registro.html')
	c = Context({'form': rform})
	c.update(csrf(request))
	return HttpResponse(t.render(c))

## -- Pago
class PagoForm(forms.Form):
	email = forms.CharField(required=False)
	code  = forms.CharField(required=False)
	file  = forms.FileField(widget=forms.FileInput, required=False)

	def clean(self):
		data = self.cleaned_data
		email = data.get("email")
		code  = data.get("code")
		person = Perfil.objects.filter(email=email).filter(code=code)
		print person
		print code
		print email
		if not person.exists():
			raise forms.ValidationError("La combinación correo y codigo no es corecto.")
		if not data.get('file'):
			raise forms.ValidationError("Adjunta un archivo")
		return self.cleaned_data


def Pago(request):
	if request.method == "POST":
		pform = PagoForm(request.POST, request.FILES)
		if pform.is_valid():
			persona = Perfil.objects.get(email=pform.cleaned_data['email'])
			handle_uploaded_file(request.FILES['file'],persona.rut)
			persona.pago = "u"
			persona.save()
			t = get_template('public/pago_done.html')
			return HttpResponse(t.render(Context()))
	else:
		pform = PagoForm()

	t = get_template('public/pago.html')
	c = Context({'form': pform})
   	c.update(csrf(request))
	return HttpResponse(t.render(c))

def handle_uploaded_file(f,rut):
	PPATH = '%s/pagos/%s' % (DEPLOY_PATH, rut)
	if not os.path.exists(PPATH):
		  os.mkdir(PPATH)
	FULLPATH = '%s/%s' % (PPATH, f.name)
	destination = open(FULLPATH, 'wb+')
	for chunk in f.chunks():
		destination.write(chunk)
	destination.close()

## -- Lista
def Lista(request):
	personas = Perfil.objects.filter(confirmado=True)
	t = get_template('public/listas.html')
	c = Context({'personas': personas})
	return HttpResponse(t.render(c))

## -- Home
def Home(request):
	 t = get_template('public/index.html')
	 return HttpResponse(t.render(Context()))
    
