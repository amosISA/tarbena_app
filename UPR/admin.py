from django.contrib import admin

# Register your models here.

from .models import Maquina, TipoMaquina, Componentes, Incidencias, GrupoComponentes, Poblacion, Comarca, Provincia, MovimientoMaquinaria, RevisionesTemporada


## POBLACIONES, COMARCAS Y PROVINCIAS
##
class PoblacionAdmin(admin.ModelAdmin):
    list_display = ('nombre','codigo_INE',)
    list_filter = ('nombre','codigo_INE',)
    search_fields = ('nombre','codigo_INE')
    empty_value_display = '-'
    list_display_links = ('nombre',)
    show_full_result_count = True
admin.site.register(Poblacion, PoblacionAdmin)

class ComarcaAdmin(admin.ModelAdmin):
    list_display = ('nombre','capital','habitantes','km_cuadrados',)
    list_filter = ('nombre',)
    search_fields = ('nombre',)
    empty_value_display = '-'
    list_display_links = ('nombre',)
    show_full_result_count = True
admin.site.register(Comarca, ComarcaAdmin)

class ProvinciaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    list_filter = ('nombre',)
    search_fields = ('nombre',)
    empty_value_display = '-'
    list_display_links = ('nombre',)
    show_full_result_count = True
admin.site.register(Provincia, ProvinciaAdmin)


class MaquinaAdmin(admin.ModelAdmin):
    list_display = ('numero_inventario', 'numero_serie', 'fecha_compra','tipo_maquina','capataz_responsable',)
    list_filter = ['tipo_maquina__tipo', 'numero_inventario',]
    search_fields = ('numero_inventario', 'numero_serie', 'tipo_maquina',)
    empty_value_display = '-'
    list_display_links = ('numero_inventario',)
    show_full_result_count = True

#    def nombre_poblacion_display(self, obj):
#        return ", ".join([
#            poblacion.nombre for poblacion in obj.nombre.all()
#        ])
#    nombre_poblacion_display.short_description = "nombre poblacion"
admin.site.register(Maquina, MaquinaAdmin)

class TipoMaquinaAdmin(admin.ModelAdmin):
    list_display = ('tipo',)
    list_filter = ['tipo']
    search_fields = ('tipo',)
    empty_value_display = '-'
    list_display_links = ('tipo',)
    show_full_result_count = True
admin.site.register(TipoMaquina, TipoMaquinaAdmin)

class GrupoComponentesAdmin(admin.ModelAdmin):
    list_display = ('tipo_grupo_componentes','position_grupo_componentes',)
    list_filter = ['tipo_grupo_componentes']
    search_fields = ('tipo_grupo_componentes',)
    empty_value_display = '-'
    list_display_links = ('tipo_grupo_componentes',)
    show_full_result_count = True
admin.site.register(GrupoComponentes, GrupoComponentesAdmin)

class ComponentesAdmin(admin.ModelAdmin):
    list_display = ('tipo_componentes','tipo_comentario','imatge_componente','tipo_maquina_display','grupo_componentes',)
    list_filter = ['tipo_componentes']
    search_fields = ('tipo_componentes',)
    empty_value_display = '-'
    list_display_links = ('tipo_componentes',)
    show_full_result_count = True

    def tipo_maquina_display(self, obj):
        return ", ".join([
            maquina.tipo for maquina in obj.tipo_maquina.all()
        ])
    tipo_maquina_display.short_description = "Tipo maquina"

#    def position_grupo_componentes_display(self, obj):
#        return ", ".join([
#            grupoComponentes.
#        ])
admin.site.register(Componentes, ComponentesAdmin)

class IncidenciasAdmin(admin.ModelAdmin):
    list_display = ('tipo_incidencias','fecha','comentario',)
    list_filter = ('tipo_incidencia', 'tipo_incidencia__tipo_maquina',)
    search_fields = ('tipo_incidencias',)
    empty_value_display = '-'
    list_display_links = ('tipo_incidencias',)
    show_full_result_count = True
admin.site.register(Incidencias, IncidenciasAdmin)


class MovimientoMaquinariaAdmin(admin.ModelAdmin):
    list_display = ('numero_inventario_mm','poblacion_mm','fecha_movimiento',)
    list_filter = ('numero_inventario_mm', 'poblacion_mm',)
    search_fields = ('numero_inventario_mm',)
    empty_value_display = '-'
    list_display_links = ('numero_inventario_mm',)
    show_full_result_count = True
admin.site.register(MovimientoMaquinaria, MovimientoMaquinariaAdmin)

class RevisionesTemporadaAdmin(admin.ModelAdmin):
    list_display = ('nombre_revision','fecha_revision',)
    list_filter = ('nombre_revision', 'fecha_revision',)
    search_fields = ('nombre_revision',)
    empty_value_display = '-'
    list_display_links = ('nombre_revision',)
    show_full_result_count = True
admin.site.register(RevisionesTemporada, RevisionesTemporadaAdmin)