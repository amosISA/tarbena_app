# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Parcela, Propietario, SectorTrabajo, Estado, Proyecto, Poblacion
from .sites import my_admin_site

class ParcelaAdmin(admin.ModelAdmin):
    list_display = ['poligono', 'numero_parcela', 'propietario', 'metros_cuadrados']
    list_filter = ['propietario__nombre', 'metros_cuadrados', 'poligono',
                    'numero_parcela']
    search_fields = ('propietario__nombre', 'metros_cuadrados', 'poligono',
                     'numero_parcela',)
    empty_value_display = '-'
    list_display_links = ('numero_parcela',)
    show_full_result_count = True
my_admin_site.register(Parcela, ParcelaAdmin)
admin.site.register(Parcela, ParcelaAdmin)

class PropietarioAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'apellidos', 'nif', 'poblacion', 'calle',
                    'telefono_fijo', 'telefono_movil', 'comentarios']
    list_filter = ['nombre', 'apellidos', 'nif', 'poblacion', 'calle',
                   'telefono_fijo', 'telefono_movil', 'comentarios']
    search_fields = ('nombre', 'apellidos', 'nif', 'poblacion', 'calle',
                     'telefono_fijo', 'telefono_movil', 'comentarios',)
    empty_value_display = '-'
    show_full_result_count = True
admin.site.register(Propietario, PropietarioAdmin)

class SectorTrabajoAdmin(admin.ModelAdmin):
    list_display = ['sector']
    list_filter = ['sector']
    search_fields = ('sector',)
    empty_value_display = '-'
    show_full_result_count = True
admin.site.register(SectorTrabajo, SectorTrabajoAdmin)

class ProyectoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'descripcion', 'comentarios']
    list_filter = ['nombre', 'descripcion', 'comentarios']
    search_fields = ('nombre', 'descripcion', 'comentarios',)
    empty_value_display = '-'
    show_full_result_count = True
admin.site.register(Proyecto, ProyectoAdmin)

class EstadoAdmin(admin.ModelAdmin):
    list_display = ['nombre']
    list_filter = ['nombre']
    search_fields = ('nombre',)
    empty_value_display = '-'
    show_full_result_count = True
admin.site.register(Estado, EstadoAdmin)

class PoblacionAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'nombre']
    list_filter = ['codigo', 'nombre']
    search_fields = ('codigo', 'nombre',)
    empty_value_display = '-'
    show_full_result_count = True
admin.site.register(Poblacion, PoblacionAdmin)
