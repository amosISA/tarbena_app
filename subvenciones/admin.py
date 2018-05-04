# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Subvencion, Estado, Colectivo, Ente, Area

# Register your models here.
class SubvencionAdmin(admin.ModelAdmin):
    list_display = ['inicio', 'nombre', 'fin', 'cuantia_inicial', 'cuantia_final',
                    'estado', 'ente', 'user']
    list_filter = ['nombre', 'estado', 'colectivo', 'cuantia_inicial', 'cuantia_final', 'ente']
    search_fields = ('nombre',)
    empty_value_display = '-' # para los campos vacios se pone eso
    list_display_links = ('nombre',) # que campo aparece como un link para editar el registro
    show_full_result_count = True

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super(SubvencionAdmin, self).save_model(request, obj, form, change)
admin.site.register(Subvencion, SubvencionAdmin)

class EstadoAdmin(admin.ModelAdmin):
    exclude = ('slug',)
admin.site.register(Estado, EstadoAdmin)

class ColectivoAdmin(admin.ModelAdmin):
    exclude = ('slug',)
admin.site.register(Colectivo, ColectivoAdmin)

class EnteAdmin(admin.ModelAdmin):
    exclude = ('slug',)
admin.site.register(Ente, EnteAdmin)

class AreaAdmin(admin.ModelAdmin):
    exclude = ('slug',)
admin.site.register(Area, AreaAdmin)

