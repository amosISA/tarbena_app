from django.contrib import admin
from django.conf.locale.es import formats

from .models import Contract, TypeContract, Contractor, AplicacionPresupuestaria, Organos

formats.DATE_FORMAT = "d/m/Y"

# Register your models here.
class ContractsAdmin(admin.ModelAdmin):
    list_display = ['identificador' ,'type', 'contractor', 'base',
                    'iva', 'total', 'date_contract']
    list_filter = ['type__name', 'contractor__name', 'date_contract']
    search_fields = ('type__name', 'contractor__name', 'date_contract',)
    empty_value_display = '-'
    list_display_links = ('contractor',)
    show_full_result_count = True

    # https://medium.com/@hakibenita/things-you-must-know-about-django-admin-as-your-app-gets-bigger-6be0b0ee9614
    list_select_related = (
        'type',
        'contractor',
    )

admin.site.register(Contract, ContractsAdmin)

class TypeContractAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_filter = ['name']
    search_fields = ['name']
    empty_value_display = '-'
    list_display_links = ('name',)
    show_full_result_count = True
admin.site.register(TypeContract, TypeContractAdmin)

class ContractorAdmin(admin.ModelAdmin):
    list_display = ['name', 'dni']
    list_filter = ['name', 'dni']
    search_fields = ['name', 'dni']
    empty_value_display = '-'
    list_display_links = ('name', 'dni',)
    show_full_result_count = True
admin.site.register(Contractor, ContractorAdmin)

class AplicacionPresupuestariaAdmin(admin.ModelAdmin):
    list_display = ['ejercicio', 'aplicacion_presupuestaria', 'importe', 'importe_recursos',
                    'valor_estimado', 'porcentaje', 'organo']
    list_filter = ['ejercicio', 'aplicacion_presupuestaria', 'importe', 'importe_recursos',
                    'valor_estimado', 'porcentaje', 'organo']
    search_fields = ['ejercicio', 'aplicacion_presupuestaria', 'importe', 'importe_recursos',
                    'valor_estimado', 'porcentaje', 'organo']
    empty_value_display = '-'
    list_display_links = ('aplicacion_presupuestaria',)
    show_full_result_count = True
admin.site.register(AplicacionPresupuestaria, AplicacionPresupuestariaAdmin)

class OrganosAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_filter = ['name']
    search_fields = ['name']
    empty_value_display = '-'
    list_display_links = ('name',)
    show_full_result_count = True
admin.site.register(Organos, OrganosAdmin)