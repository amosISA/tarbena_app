# -*- coding: utf-8 -*-
from django.contrib import admin

from import_export.admin import ImportExportModelAdmin
from .models import Parcela, Propietario, SectorTrabajo, Estado, Proyecto, Poblacion, Estado_Parcela_Trabajo, Provincia, PoblacionesFavoritas
from .sites import my_admin_site

import urllib.request
import ssl

class ParcelaInline(admin.TabularInline):
    model = Parcela
    max_num = 0
    show_change_link = True

class ParcelaAdmin(admin.ModelAdmin):
    list_display = ['poblacion' ,'poligono', 'numero_parcela', 'propietario', 'metros_cuadrados', 'estado_parcela_trabajo', 'estado']
    list_editable = ('poblacion',)
    list_filter = ['propietario__nombre', 'propietario__apellidos', 'metros_cuadrados', 'poligono',
                    'numero_parcela', 'poblacion', 'propietario__apellidos2']
    search_fields = ('propietario__nombre', 'metros_cuadrados', 'poligono',
                     'numero_parcela', 'poblacion')
    empty_value_display = '-'
    list_display_links = ('numero_parcela',)
    show_full_result_count = True

    # Make kml for each parcela
    # def save_model(self, request, obj, form, change):
    #     super(ParcelaAdmin, self).save_model(request, obj, form, change)
    #     #https://stackoverflow.com/questions/3813735/in-python-how-to-specify-a-format-when-converting-int-to-string
    #
    #     if not obj.kml:
    #         context = ssl._create_unverified_context()
    #         kml_url='https://ovc.catastro.meh.es/Cartografia/WMS/BuscarParcelaGoogle3D.aspx?refcat=03' + obj.poblacion.codigo + 'A'+ "{:03n}".format(int(obj.poligono)) + "{:05n}".format(int(obj.numero_parcela)) + '0000BP&del=3&mun=' + obj.poblacion.codigo + '&tipo=3d'
    #         fp = urllib.request.urlopen(kml_url,context=context)
    #         mybytes = fp.read()
    #         mykml = mybytes.decode('unicode_escape').encode('utf-8')
    #         print(mykml)
    #         obj.kml = mykml
    #         obj.save()
my_admin_site.register(Parcela, ParcelaAdmin)
admin.site.register(Parcela, ParcelaAdmin)

class PropietarioAdmin(ImportExportModelAdmin):
    list_display = ['nombre', 'apellidos', 'apellidos2', 'poblacion', 'direccion', 'nif',
                    'telefono_fijo', 'telefono_movil', 'comentarios']
    list_filter = ['nombre', 'apellidos', 'nif',
                   'telefono_fijo', 'telefono_movil', 'comentarios']
    list_editable = ('poblacion',)
    search_fields = ('nombre', 'apellidos', 'nif', 'poblacion',
                     'telefono_fijo', 'telefono_movil', 'comentarios',)
    empty_value_display = '-'
    show_full_result_count = True
    inlines = [ParcelaInline]
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

class EstadoParcelaTrabajoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'porcentaje']
    list_filter = ['nombre']
    search_fields = ('nombre',)
    empty_value_display = '-'
    show_full_result_count = True
admin.site.register(Estado_Parcela_Trabajo, EstadoParcelaTrabajoAdmin)

class PoblacionAdmin(ImportExportModelAdmin):
    list_display = ['codigo', 'nombre', 'provincia']
    list_filter = ['codigo', 'nombre', 'provincia']
    list_display_links = ('nombre',)
    search_fields = ('codigo', 'nombre', 'provincia',)
    empty_value_display = '-'
    show_full_result_count = True
admin.site.register(Poblacion, PoblacionAdmin)

class ProvinciaAdmin(ImportExportModelAdmin):
    list_display = ['codigo', 'nombre']
    #list_editable = ('codigo',)
    list_filter = ['codigo', 'nombre']
    list_display_links = ('nombre',)
    search_fields = ('codigo', 'nombre',)
    empty_value_display = '-'
    show_full_result_count = True
admin.site.register(Provincia, ProvinciaAdmin)

class PoblacionesFavoritasAdmin(admin.ModelAdmin):
    list_display = ['user']
    list_filter = ['user', 'poblacion']
    search_fields = ('user', 'poblacion',)
    empty_value_display = '-'
    show_full_result_count = True
admin.site.register(PoblacionesFavoritas, PoblacionesFavoritasAdmin)