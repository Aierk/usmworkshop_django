from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from main.views import Registro, Pago, Lista, Home, Lugar, Requisitos

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', Home),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^registrar/',Registro),
    url(r'^pago/', Pago),
    url(r'^lista/', Lista),
    url(r'^lugar/', Lugar),
    url(r'^requisitos/', Requisitos),
					  
)
