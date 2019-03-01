from django.contrib import admin

from .models import Terceros

# Register your models here.
class TerceroAdmin(admin.ModelAdmin):
    list_display = ['identificacion', 'nombre', 'primer_apellido', 'segundo_apellido',
                    'email', 'provincia', 'municipio']
    list_filter = ['provincia', 'municipio']
    search_fields = ('identificacion', 'nombre', 'primer_apellido', 'segundo_apellido',
                     'movil', 'telefono', 'fax', 'email', 'pagina_web', 'tipo_via',
                     'nombre_via', 'numero', 'bloque', 'escalera', 'planta', 'puerta',
                     'pais', 'provincia', 'municipio', 'codigo_postal',)
    empty_value_display = '-'
    show_full_result_count = True

admin.site.register(Terceros, TerceroAdmin)