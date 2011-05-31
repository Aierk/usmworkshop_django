# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin

SKILLS_CHOICES = (
	('n','Nada en Particular'),
	('d','Diseñador de Juego o Niveles'),
	('a','Artista 3D'),
	('c','Programador'),
	('i','Ilustrador'),
	('m','Compositor Musical'),
	
	)

PAGO_CHOICES = (
	('u', 'UPLOADED'),
	('n', 'NOT YET'),
	)

class Perfil(models.Model):
	nombre = models.CharField(max_length=20, blank=False)
	apellido = models.CharField(max_length=20, blank=False)
	email = models.EmailField(blank=False)
	rut  = models.CharField(max_length=10, blank=False)
	fono = models.CharField(max_length=15, blank=True)
	organizacion = models.CharField(max_length=50)
	notebook = models.BooleanField(default=False)
	equipo = models.CharField(max_length=50)
	skill = models.CharField(max_length=1, choices=SKILLS_CHOICES, default='n')
	confirmado = models.BooleanField(default=False)
	pago = models.CharField(max_length=1, blank=True, default='n', choices=PAGO_CHOICES)
	reg_date = models.DateTimeField(auto_now_add=True)
	code = models.CharField(max_length=5)
	estudiante = models.BooleanField(default=True)

	def __unicode__(self):
		return u'%s %s <%s>' % (self.nombre, self.apellido, self.email)

	class Meta:
		ordering = ['-apellido']

	def email_enc(self):
		return u'%s' % (self.email.replace('@','_AT_'))

User.profile = property(lambda u: Perfil.objects.get_or_create(user=u)[0])

class PerfilAdmin(admin.ModelAdmin):
	search_fields = ["rut","nombre","apellido"]

admin.site.register(Perfil,PerfilAdmin)


