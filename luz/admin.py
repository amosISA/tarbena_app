from django.contrib import admin

from .models import Contador, Factura

# Register your models here.
class ContadorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion', 'codigo',)
    list_filter = ['nombre']
    search_fields = ('nombre', 'descripcion', 'codigo',)
    empty_value_display = '-'
    list_display_links = ('nombre',)
    show_full_result_count = True
admin.site.register(Contador, ContadorAdmin)

class FacturaAdmin(admin.ModelAdmin):
    list_display = ('desde', 'hasta', 'cantidad', 'lectura_anterior', 'lectura_posterior', 'consumo',)
    list_filter = ['contador__nombre', 'desde', 'hasta', 'cantidad', 'lectura_anterior', 'lectura_posterior', 'consumo']
    search_fields = ('contador__nombre' ,'desde', 'hasta', 'cantidad', 'lectura_anterior', 'lectura_posterior', 'consumo',)
    empty_value_display = '-'
    list_display_links = ('desde',)
    show_full_result_count = True
    date_hierarchy = 'desde'
    list_select_related = (
        'contador',
    )
admin.site.register(Factura, FacturaAdmin)