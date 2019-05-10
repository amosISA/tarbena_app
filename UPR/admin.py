from django.contrib import admin

# Register your models here.

from .models import Maquina, TipoMaquina, Componentes, Incidencias

class MaquinaAdmin(admin.ModelAdmin):
    list_display = ('numero_inventario', 'numero_serie', 'fecha_compra','tipo_maquina','capataz_responsable',)
    list_filter = ['tipo_maquina__tipo', 'numero_inventario',]
    search_fields = ('numero_inventario', 'numero_serie', 'tipo_maquina',)
    empty_value_display = '-'
    list_display_links = ('numero_inventario',)
    show_full_result_count = True

admin.site.register(Maquina, MaquinaAdmin)

class TipoMaquinaAdmin(admin.ModelAdmin):
    list_display = ('tipo',)
    list_filter = ['tipo']
    search_fields = ('tipo',)
    empty_value_display = '-'
    list_display_links = ('tipo',)
    show_full_result_count = True

admin.site.register(TipoMaquina, TipoMaquinaAdmin)

class ComponentesAdmin(admin.ModelAdmin):
    list_display = ('tipo_componentes',)
    list_filter = ['tipo_componentes']
    search_fields = ('tipo_componentes',)
    empty_value_display = '-'
    list_display_links = ('tipo_componentes',)
    show_full_result_count = True

admin.site.register(Componentes, ComponentesAdmin)

class IncidenciasAdmin(admin.ModelAdmin):
    list_display = ('tipo_incidencias','fecha','comentario',)
    list_filter = ('tipo_incidencia', 'tipo_incidencia__tipo_maquina',)
    search_fields = ('tipo_incidencias',)
    empty_value_display = '-'
    list_display_links = ('tipo_incidencias',)
    show_full_result_count = True

admin.site.register(Incidencias, IncidenciasAdmin)