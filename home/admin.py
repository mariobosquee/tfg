from django.contrib import admin
from .models import (
    Actividad, Antecedente,
    Ccaa, Causa,
    Deteccion, Extraccion,
    Factorriesgo,
    Incidente, Intervencion,
    Localidad, Localizacion,
    Materialrescate, Nacionalidad,
    Origen, Primerinterviniente,
    Pronostico, Provincia,
    Reanimacion, Riesgo,
    Tipoahogamiento,
    Victima,
    Zonavigilada,
)


admin.site.register(Actividad)
admin.site.register(Antecedente)
admin.site.register(Ccaa)
admin.site.register(Causa)
admin.site.register(Deteccion)
admin.site.register(Extraccion)
admin.site.register(Factorriesgo)
admin.site.register(Incidente)
admin.site.register(Intervencion)
admin.site.register(Localidad)
admin.site.register(Localizacion)
admin.site.register(Materialrescate)
admin.site.register(Nacionalidad)
admin.site.register(Origen)
admin.site.register(Primerinterviniente)
admin.site.register(Pronostico)
admin.site.register(Provincia)
admin.site.register(Reanimacion)
admin.site.register(Riesgo)
admin.site.register(Tipoahogamiento)
admin.site.register(Victima)
admin.site.register(Zonavigilada)