from django.contrib import admin

from .models import Contract, TypeContract, Contractor

# Register your models here.
class ContractsAdmin(admin.ModelAdmin):
    list_display = ['type', 'contractor', 'base',
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