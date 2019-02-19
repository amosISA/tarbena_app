from django.contrib import admin
from django.conf.locale.es import formats
from django.http import HttpResponse

from .models import Contract, TypeContract, Contractor, AplicacionPresupuestaria, Organos, Cpv

import xlwt
import datetime

formats.DATE_FORMAT = "d/m/Y"

def export_xls(modeladmin, request, queryset):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=contratos.xls'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet("Contratos")

    row_num = 0

    columns = [
        ('Tipo', 3500), ('Contratista', 10000), ('Base', 2400),
        ('IVA', 2300), ('Total', 2400), ('Fecha', 2500)
    ]

    font_style = xlwt.easyxf('align: wrap yes,vert centre, horiz center; \
                                   border: left thin,right thin,top thin,bottom thin')
    font_style.font.bold = True
    font_style.alignment.wrap = 1

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num][0], font_style)
        # set column width
        ws.col(col_num).width = columns[col_num][1]

    font_style = xlwt.XFStyle()
    font_style.alignment.wrap = 1

    for obj in queryset:
        row_num += 1
        row = [
            obj.type.name,
            obj.contractor.name,
            obj.base.replace("€","").replace(" ",""),
            obj.iva.replace("€","").replace(" ",""),
            obj.total.replace("€","").replace(" ",""),
            obj.date_contract,
        ]
        for col_num in range(len(row)):
            if isinstance(row[col_num], datetime.date):
                font_style = xlwt.easyxf('border: left thin,right thin,top thin,bottom thin\
                                                     ', num_format_str='DD-MM-YYYY')
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response

export_xls.short_description = "Exportar a Excel"

class ContractsAdmin(admin.ModelAdmin):
    list_display = ['type', 'contractor', 'base',
                    'iva', 'total', 'date_contract']
    list_filter = ['type__name', 'contractor__name', 'date_contract']
    #list_editable = ('date_contract',)
    search_fields = ('type__name', 'contractor__name', 'date_contract',)
    empty_value_display = '-'
    list_display_links = ('contractor',)
    show_full_result_count = True
    #raw_id_fields = ("cpv",)
    date_hierarchy = 'date_contract'

    actions = [export_xls]

    # https://medium.com/@hakibenita/things-you-must-know-about-django-admin-as-your-app-gets-bigger-6be0b0ee9614
    list_select_related = (
        'type',
        'contractor',
        'aplic_presupuestaria',
        'organo',
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
    list_display = ['aplicacion_presupuestaria']
    list_filter = ['aplicacion_presupuestaria']
    search_fields = ['aplicacion_presupuestaria']
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

class CpvAdmin(admin.ModelAdmin):
    list_display = ['cpv']
    list_filter = ['cpv']
    search_fields = ['cpv']
    empty_value_display = '-'
    list_display_links = ('cpv',)
    show_full_result_count = True
admin.site.register(Cpv, CpvAdmin)